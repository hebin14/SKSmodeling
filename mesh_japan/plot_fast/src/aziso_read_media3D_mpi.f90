module constants 

! constants defined
integer,PARAMETER   :: NGLLX = 5,NGLLY = NGLLX, NGLLZ = NGLLX 
integer,PARAMETER   :: CUSTOM_REAL = 4,DOUBLE_REAL = 8
integer,PARAMETER   :: UTM_PROJECTION_ZONE = 54
integer,parameter   :: MAX_STR_LEN = 256
integer,PARAMETER     :: IIN = 10,IOUT = 20

contains 

subroutine get_lines(filename,npts)
  implicit none
  
  character(len=MAX_STR_LEN) :: filename 
  integer,intent(inout)      :: npts 

  ! local
  character(len=MAX_STR_LEN) :: line 
  integer                    :: ierr 

  ! read until endoffile
  npts = 0
  open(IIN,file=filename)
  do 
    read(IIN,*,iostat=ierr) line
    if(ierr /= 0) exit 
    npts = npts + 1
  enddo
  close(IIN)

end subroutine get_lines

subroutine min_allprocs(vpmin_slice,distmin_slice,vpout,distout,npts)
  use mpi_f08
  implicit none
  integer,intent(in)   :: npts
  real(kind=CUSTOM_REAL),intent(in)    :: vpmin_slice(npts),distmin_slice(npts)
  real(kind=CUSTOM_REAL),intent(inout) :: vpout(npts),distout(npts)

  ! local
  integer                 :: myrank,ierr,ipt
  real(kind=CUSTOM_REAL)  :: distin(2,npts),distall(2,npts),vmin(npts),dmin(npts)

  ! get current rank 
  call MPI_COMM_RANK(MPI_COMM_WORLD, myrank,ierr)

  ! find min distance in global
  distin(1,:) = distmin_slice(:)
  distin(2,:) = real(myrank,kind=CUSTOM_REAL)

  ! find minloc
  call MPI_ALLREDUCE(distin,distall,npts,MPI_2REAL,MPI_MINLOC,MPI_COMM_WORLD,ierr)
  vmin(:) = 0.0_CUSTOM_REAL
  dmin(:) = 0.0_CUSTOM_REAL

  do ipt=1,npts 
    if(myrank == int(distall(2,ipt))) then 
      vmin(ipt) = vpmin_slice(ipt)
      dmin(ipt) = distmin_slice(ipt)
    endif
  enddo
  
  call MPI_Reduce(vmin,vpout,npts,MPI_REAL,MPI_SUM,0,MPI_COMM_WORLD,ierr)
  call MPI_Reduce(dmin,distout,npts,MPI_REAL,MPI_SUM,0,MPI_COMM_WORLD,ierr)

end subroutine min_allprocs

end module constants 


! BinHe
! put vpv vph vsv vsh density gc gs into single files to reduce file numbers
! for azimuthal anisotropy, provide binary files including: vpv vph vsv vsh density gc gs

program main 
  use mpi_f08
  use constants
  implicit none

  ! filename
  character(len=MAX_STR_LEN)  :: COOR_PATH,MODEL_PATH,INTFILE,parname,out_name,filename
  
  ! useful arrays
  real(kind=CUSTOM_REAL),ALLOCATABLE   :: vpv_read(:,:,:,:),vph_read(:,:,:,:),vsv_read(:,:,:,:)
  real(kind=CUSTOM_REAL),ALLOCATABLE   :: vsh_read(:,:,:,:),rho_read(:,:,:,:),gc_read(:,:,:,:),gs_read(:,:,:,:)  ! parameter
  
  integer,ALLOCATABLE :: ibool(:,:,:,:)   ! global index
  real(kind=CUSTOM_REAL),DIMENSION(:),ALLOCATABLE   :: xstore,ystore,zstore

  ! interpolated coordinates
  real(kind=CUSTOM_REAL),ALLOCATABLE  :: xint(:),yint(:),zint(:),vpvint(:),vphint(:)
  real(kind=CUSTOM_REAL),ALLOCATABLE  :: vsvint(:),vshint(:),rhoint(:),gcint(:),gsint(:)

  real(kind=CUSTOM_REAL),ALLOCATABLE  :: dist(:),distmin(:),vpvmin(:),vsvmin(:),rhomin(:)
  real(kind=CUSTOM_REAL),ALLOCATABLE  :: vphmin(:),vshmin(:),gcmin(:),gsmin(:)
  integer             :: npts 

  integer     :: nspec,nglob,i,j,k,ispec,iglob,nspec_ire,ierr,ipt 

  ! mpi parameters
  integer     :: rank,nproc

  ! temp
  real(kind=8)  :: rlon,rlat,rx,ry

  ! mpi init
  call MPI_INIT(ierr)
  call MPI_COMM_SIZE(MPI_COMM_WORLD, nproc, ierr)
  call MPI_COMM_RANK(MPI_COMM_WORLD, rank,ierr)

  ! get input args
  if(rank == 0) then 
    if(command_argument_count() /= 4) then 
      print *,'Usage :'
      stop './runthis COOR_PATH MODEL_PATH INFILE out_name'
    else 
      call get_command_argument(1,COOR_PATH)
      call get_command_argument(2,MODEL_PATH)
      COOR_PATH = trim(COOR_PATH)
      MODEL_PATH = trim(MODEL_PATH)
      call get_command_argument(3,INTFILE)
      INTFILE = trim(INTFILE)
      call get_command_argument(4,out_name)
      out_name = trim(out_name)
      write(*,'(a,a)') 'COOR_PATH = ',adjustl(trim(COOR_PATH))
      write(*,'(a,a)') 'MODEL_PATH = ',adjustl(trim(MODEL_PATH))      
      write(*,'(a,a)') 'input points file = ',adjustl(trim(INTFILE))
      write(*,'(a,a)') 'output ascii file = ',adjustl(trim(out_name))      
    endif
  endif 
  
  ! bcast parameters to file
  call MPI_Bcast(COOR_PATH,MAX_STR_LEN,MPI_CHARACTER,0,MPI_COMM_WORLD)
  call MPI_Bcast(MODEL_PATH,MAX_STR_LEN,MPI_CHARACTER,0,MPI_COMM_WORLD)
  call MPI_Bcast(INTFILE,MAX_STR_LEN,MPI_CHARACTER,0,MPI_COMM_WORLD)
  call MPI_Bcast(out_name,MAX_STR_LEN,MPI_CHARACTER,0,MPI_COMM_WORLD)

  !read nspec and nglob
  write(filename,'(a,a,i6.6,a)') trim(COOR_PATH),'/proc',rank,'_external_mesh.bin'
  open(IIN,file=trim(filename),form='unformatted')
  read(IIN) nspec 
  read(IIN) nglob 
  read(IIN) nspec_ire
  
  ! allocate space
  ALLOCATE(ibool(NGLLX,NGLLY,NGLLZ,nspec),stat=ierr)
  ALLOCATE(xstore(nglob),ystore(nglob),zstore(nglob))
  
  ! read x,y,z,ibool
  read(IIN) ibool
  read(IIN) xstore; read(IIN) ystore; read(IIN) zstore;
  close(IIN)
  allocate(vpv_read(NGLLX,NGLLY,NGLLZ,nspec),vph_read(NGLLX,NGLLY,NGLLZ,nspec))
  allocate(vsv_read(NGLLX,NGLLY,NGLLZ,nspec),vsh_read(NGLLX,NGLLY,NGLLZ,nspec))
  allocate(gc_read(NGLLX,NGLLY,NGLLZ,nspec),gs_read(NGLLX,NGLLY,NGLLZ,nspec))
  allocate(rho_read(NGLLX,NGLLY,NGLLZ,nspec))
  
  !read vp
  write(filename,'(a,a,i6.6,a,a,a)') trim(MODEL_PATH),'/proc',rank,'_vpvhvsvhrhogcgs.bin'
  open(IIN,file=trim(filename),form='unformatted',iostat=ierr)
  if(ierr /=0 ) stop 'error readind vpvhvsvhrhogcgs.bin '
  read(IIN) vpv_read,vph_read,vsv_read,vsh_read,rho_read,gc_read,gs_read
  close(IIN)
  if(rank == 0)  then 
    write(filename,'(a,a,a,a,a)') trim(MODEL_PATH),'/proc','_vpvhvsvhrhogcgs.bin'
    print*,'finished reading parameters '//trim(filename)
  endif

  ! read interpolated points
  call get_lines(INTFILE,npts)
  ALLOCATE(xint(npts),yint(npts),zint(npts))
  allocate(vpvint(npts),vphint(npts),vsvint(npts),vshint(npts),gsint(npts),gcint(npts))
  allocate(rhoint(npts),dist(npts),distmin(npts))
  allocate(vpvmin(npts),vphmin(npts),vsvmin(npts),vshmin(npts),rhomin(npts),gsmin(npts),gcmin(npts))

  open(IIN,file=INTFILE)
  do i=1,npts 
    read(IIN,*)rlon,rlat,zint(i)
    call utm_geo(rlon,rlat,rx,ry,UTM_PROJECTION_ZONE,0) ! geo2utm
    xint(i) = real(rx,kind=CUSTOM_REAL)
    yint(i) = real(ry,kind=CUSTOM_REAL)
  enddo
  close(IIN)
  if(rank == 0)  then 
    print*,'finished reading coordinates'
    print*,'min/max x range:',minval(xint),maxval(xint)
    print*,'min/max y range:',minval(yint),maxval(yint)
    print*,'min/max z range:',minval(zint),maxval(zint)
  endif

  ! find the nearest point in this proc
  distmin(:) = huge(xint(1))
  do ispec = 1,nspec 
    do k=1,NGLLZ 
      do j=1,NGLLY 
        do i=1,NGLLX
          iglob = ibool(i,j,k,ispec)
          dist(:) = sqrt((xint(1:npts)-xstore(iglob))**2 &
                    +(yint(1:npts)-ystore(iglob))**2 &
                    +(zint(1:npts)-zstore(iglob))**2)
          do ipt=1,npts 
            if (dist(ipt) < distmin(ipt)) then 
              vpvmin(ipt) = vpv_read(i,j,k,ispec)
              vphmin(ipt) = vph_read(i,j,k,ispec)
              vsvmin(ipt) = vsv_read(i,j,k,ispec)
              vshmin(ipt) = vsh_read(i,j,k,ispec)
              rhomin(ipt) = rho_read(i,j,k,ispec)
              gcmin(ipt)  = gc_read(i,j,k,ispec)
              gsmin(ipt)  = gs_read(i,j,k,ispec)
              distmin(ipt) = dist(ipt)
            endif 
          enddo
        enddo
      enddo
    enddo
  enddo
  if(rank == 0)  then 
    print*,'finished finding local distmin'
  endif
  call MPI_BARRIER(MPI_COMM_WORLD,ierr)

  ! find the parameters for the nearest point in global
  call min_allprocs(vpvmin,distmin,vpvint,dist,npts)
  call min_allprocs(vphmin,distmin,vphint,dist,npts)
  call min_allprocs(vsvmin,distmin,vsvint,dist,npts)
  call min_allprocs(vshmin,distmin,vshint,dist,npts)
  call min_allprocs(rhomin,distmin,rhoint,dist,npts)
  call min_allprocs(gcmin,distmin,gcint,dist,npts)
  call min_allprocs(gsmin,distmin,gsint,dist,npts)

  ! write file
  if(rank == 0) then 
    print *, 'Writing out gmt file ...'
    open(IOUT,file=out_name)
    do ipt=1,npts 
      rx = dble(xint(ipt)); ry = dble(yint(ipt))
      call utm_geo(rlon,rlat,rx,ry,UTM_PROJECTION_ZONE,1) ! geo2utm
      write(IOUT,'(7f12.5)')vpvint(ipt),vphint(ipt),vsvint(ipt),vshint(ipt),rhoint(ipt),gcint(ipt),gsint(ipt)
    enddo
    close(IOUT)
  endif

  ! deallocate space
  DEALLOCATE(xstore,ystore,zstore,ibool)
  DEALLOCATE(xint,yint,zint,dist,distmin)
  deallocate(vpvmin,vphmin,vshmin,vsvmin,rhomin,gcmin,gsmin)
  deallocate(vpvint,vphint,vshint,vsvint,rhoint,gcint,gsint)
  deallocate(vpv_read,vph_read,vsv_read,vsh_read,rho_read,gc_read,gs_read)

  ! close output file
  close(IOUT)

  call MPI_Barrier(MPI_COMM_WORLD)

  call MPI_FINALIZE(ierr)
  
end program main 
