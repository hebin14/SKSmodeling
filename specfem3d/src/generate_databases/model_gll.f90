!=====================================================================
!
!               S p e c f e m 3 D  V e r s i o n  3 . 0
!               ---------------------------------------
!
!     Main historical authors: Dimitri Komatitsch and Jeroen Tromp
!                              CNRS, France
!                       and Princeton University, USA
!                 (there are currently many more authors!)
!                           (c) October 2017
!
! This program is free software; you can redistribute it and/or modify
! it under the terms of the GNU General Public License as published by
! the Free Software Foundation; either version 3 of the License, or
! (at your option) any later version.
!
! This program is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
! GNU General Public License for more details.
!
! You should have received a copy of the GNU General Public License along
! with this program; if not, write to the Free Software Foundation, Inc.,
! 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
!
!=====================================================================

!--------------------------------------------------------------------------------------------------
!
! GLL
!
! based on modified GLL mesh output from mesher
!
! used for iterative inversion procedures
!
!--------------------------------------------------------------------------------------------------
  ! Bin He added, leave this for isotropic gll model
  subroutine model_gll(myrank,nspec,LOCAL_PATH)

  use constants, only: NGLLX,NGLLY,NGLLZ,FOUR_THIRDS,IMAIN,MAX_STRING_LEN,IIN

  use generate_databases_par, only: ATTENUATION

  use create_regions_mesh_ext_par, only: rhostore,kappastore,mustore,rho_vp,rho_vs,qkappa_attenuation_store,qmu_attenuation_store

  implicit none

  integer, intent(in) :: myrank,nspec
  character(len=MAX_STRING_LEN) :: LOCAL_PATH

  ! local parameters
  real, dimension(:,:,:,:),allocatable :: vp_read,vs_read,rho_read
  integer :: ier
  character(len=MAX_STRING_LEN) :: prname_lp,filename

  ! user output
  if (myrank == 0) then
    write(IMAIN,*) '     using GLL model from: ',trim(LOCAL_PATH)
  endif

  ! processors name
  write(prname_lp,'(a,i6.6,a)') trim(LOCAL_PATH)// '/' //'proc',myrank,'_'
 

  ! density
  allocate(rho_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
  if (ier /= 0) call exit_MPI_without_rank('error allocating array 647')
  if (ier /= 0) stop 'error allocating array rho_read'

  ! vp
  allocate(vp_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
  if (ier /= 0) call exit_MPI_without_rank('error allocating array 648')
  if (ier /= 0) stop 'error allocating array vp_read'

 ! vs
  allocate(vs_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
  if (ier /= 0) call exit_MPI_without_rank('error allocating array 649')
  if (ier /= 0) stop 'error allocating array vs_read'

  ! user output
  if (myrank == 0) write(IMAIN,*) '     reading in: vpvsrho.bin'

  filename = prname_lp(1:len_trim(prname_lp))//'vpvsrho.bin'
  open(unit=IIN,file=trim(filename),status='old',action='read',form='unformatted',iostat=ier)
  if (ier /= 0) then
    print *,'error opening file: ',trim(filename)
    stop 'error reading rho.bin file'
  endif

  read(IIN) vp_read,vs_read,rho_read
  close(IIN)

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !!! in cases where density structure is not given
  !!! modify according to your desire

  !  rho_read = 1000.0
  !  where ( mustore > 100.0 )  &
  !           rho_read = (1.6612 * (vp_read / 1000.0)     &
  !                      -0.4720 * (vp_read / 1000.0)**2  &
  !                      +0.0671 * (vp_read / 1000.0)**3  &
  !                      -0.0043 * (vp_read / 1000.0)**4  &
  !                      +0.000106*(vp_read / 1000.0)**5)*1000.0

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !!! in cases where shear wavespeed structure is not given
  !!! modify according to your desire

  !   vs_read = 0.0
  !   where ( mustore > 100.0 )       vs_read = vp_read / sqrt(3.0)

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !!! update arrays that will be saved and used in the solver xspecfem3D
  !!! the following part is neccessary if you uncommented something above

  ! density
  rhostore(:,:,:,:) = rho_read(:,:,:,:)

  ! bulk moduli: kappa = rho * (vp**2 - 4/3 vs**2)
  kappastore(:,:,:,:) = rhostore(:,:,:,:) * ( vp_read(:,:,:,:) * vp_read(:,:,:,:) &
                                              - FOUR_THIRDS * vs_read(:,:,:,:) * vs_read(:,:,:,:) )

  ! shear moduli: mu = rho * vs**2
  mustore(:,:,:,:) = rhostore(:,:,:,:) * vs_read(:,:,:,:) * vs_read(:,:,:,:)

  ! products rho*vp and rho*vs (used to speed up absorbing boundaries contributions)
  rho_vp(:,:,:,:) = rhostore(:,:,:,:) * vp_read(:,:,:,:)
  rho_vs(:,:,:,:) = rhostore(:,:,:,:) * vs_read(:,:,:,:)

  ! gets attenuation arrays from files
  if (ATTENUATION) then
    ! shear attenuation
    ! user output
    if (myrank == 0) write(IMAIN,*) '     reading in: qmu.bin'

    filename = prname_lp(1:len_trim(prname_lp))//'qmu.bin'
    open(unit=IIN,file=trim(filename),status='old',action='read',form='unformatted',iostat=ier)
    if (ier /= 0) then
      print *,'Error opening file: ',trim(filename)
      stop 'Error reading qmu.bin file'
    endif

    read(IIN) qmu_attenuation_store
    close(IIN)

    ! bulk attenuation
    ! user output
    if (myrank == 0) write(IMAIN,*) '     reading in: qkappa.bin'

    filename = prname_lp(1:len_trim(prname_lp))//'qkappa.bin'
    open(unit=IIN,file=trim(filename),status='old',action='read',form='unformatted',iostat=ier)
    if (ier /= 0) then
      print *,'error opening file: ',trim(filename)
      stop 'error reading qkappa.bin file'
    endif

    read(IIN) qkappa_attenuation_store
    close(IIN)
  endif

  ! free memory
  deallocate(rho_read,vp_read,vs_read)

  end subroutine model_gll


  ! Bin He added, leave this for isotropic gll model
  subroutine model_gll_aniso(myrank,nspec,LOCAL_PATH)

    use constants, only: NGLLX,NGLLY,NGLLZ,FOUR_THIRDS,IMAIN,MAX_STRING_LEN,IIN
  
    use generate_databases_par, only: ATTENUATION,TRANSVERSE_ANISOTROPY,AZIMUTH_ANISOTROPY
  
    use create_regions_mesh_ext_par, only: rhostore,c11store,c12store,c13store,c14store,c15store,c16store,&
                                                             c22store,c23store,c24store,c25store,c26store,&
                                                             c33store,c34store,c35store,c36store,c44store, &
                                                             c45store,c46store,c55store,c56store,c66store
  
    implicit none
  
    integer, intent(in) :: myrank,nspec
    character(len=MAX_STRING_LEN) :: LOCAL_PATH
  
    ! local parameters
    real, dimension(:,:,:,:),allocatable :: vpv_read,vph_read,rho_read,vsv_read,vsh_read,gc_read,gs_read
    real, dimension(:,:,:,:),allocatable :: c11_read,c12_read,c13_read,c14_read,c15_read,c16_read,c22_read,c23_read, &
                                            c24_read,c25_read,c26_read,c33_read,c34_read,c35_read,c36_read,c44_read, &
                                            c45_read,c46_read,c55_read,c56_read,c66_read
    integer :: ier,i,j,k,ispec
    character(len=MAX_STRING_LEN) :: prname_lp,filename
    
    ! user output
    if (myrank == 0) then
      write(IMAIN,*) '     using GLL model from: ',trim(LOCAL_PATH)
    endif
  
    ! processors name
    write(prname_lp,'(a,i6.6,a)') trim(LOCAL_PATH)// '/' //'proc',myrank,'_'
   
  
    ! density gc and gs
    allocate(rho_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(gc_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(gs_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    if (ier /= 0) call exit_MPI_without_rank('error allocating array 647')
    if (ier /= 0) stop 'error allocating array rho, gc, gs read'
  
    ! vp vs
    allocate(vpv_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(vph_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(vsv_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(vsh_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    if (ier /= 0) call exit_MPI_without_rank('error allocating array 648')
    if (ier /= 0) stop 'error allocating array vp, vs read'
  
    ! c21
    
    allocate(c11_read(NGLLX,NGLLY,NGLLZ,nspec),c12_read(NGLLX,NGLLY,NGLLZ,nspec),c13_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(c14_read(NGLLX,NGLLY,NGLLZ,nspec),c15_read(NGLLX,NGLLY,NGLLZ,nspec),c16_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(c22_read(NGLLX,NGLLY,NGLLZ,nspec),c23_read(NGLLX,NGLLY,NGLLZ,nspec),c24_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(c25_read(NGLLX,NGLLY,NGLLZ,nspec),c26_read(NGLLX,NGLLY,NGLLZ,nspec),c33_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(c34_read(NGLLX,NGLLY,NGLLZ,nspec),c35_read(NGLLX,NGLLY,NGLLZ,nspec),c36_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(c44_read(NGLLX,NGLLY,NGLLZ,nspec),c45_read(NGLLX,NGLLY,NGLLZ,nspec),c46_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    allocate(c55_read(NGLLX,NGLLY,NGLLZ,nspec),c56_read(NGLLX,NGLLY,NGLLZ,nspec),c66_read(NGLLX,NGLLY,NGLLZ,nspec),stat=ier)
    if (ier /= 0) call exit_MPI_without_rank('error allocating array 649')
    if (ier /= 0) stop 'error allocating array vs_read'
      
    
    if(TRANSVERSE_ANISOTROPY)then
      ! user output
      if (myrank == 0) write(IMAIN,*) '     reading in: vpvhvsvhrho.bin'
      filename = prname_lp(1:len_trim(prname_lp))//'vpvhvsvhrho.bin'
      open(unit=IIN,file=trim(filename),status='old',action='read',form='unformatted',iostat=ier)
      if (ier /= 0) then
        print *,'error opening file: ',trim(filename)
        stop 'error reading vpvhvsvhrho.bin file'
      endif
      read(IIN) vpv_read,vph_read,vsv_read,vsh_read,rho_read
      close(IIN)
      do ispec=1,nspec
        do k=1,NGLLZ
          do j=1,NGLLY
            do i=1,NGLLX
              call aniso_model_to_C21(vpv_read(i,j,k,ispec),vph_read(i,j,k,ispec),vsv_read(i,j,k,ispec),vsh_read(i,j,k,ispec),&
                                      rho_read(i,j,k,ispec),0.,0.,c11store(i,j,k,ispec),c12store(i,j,k,ispec),c13store(i,j,k,ispec),&
                                      c14store(i,j,k,ispec),c15store(i,j,k,ispec),c16store(i,j,k,ispec),c22store(i,j,k,ispec),&
                                      c23store(i,j,k,ispec),c24store(i,j,k,ispec),c25store(i,j,k,ispec),c26store(i,j,k,ispec),&
                                      c33store(i,j,k,ispec),c34store(i,j,k,ispec),c35store(i,j,k,ispec),c36store(i,j,k,ispec),&
                                      c44store(i,j,k,ispec),c45store(i,j,k,ispec),c46store(i,j,k,ispec),c55store(i,j,k,ispec),&
                                      c56store(i,j,k,ispec),c66store(i,j,k,ispec))
            enddo
          enddo
        enddo
      enddo
      !rhostore = rho_read
    else if(AZIMUTH_ANISOTROPY)then
      if (myrank == 0) write(IMAIN,*) '     reading in: vpvhvsvhrhogcgs.bin'
      filename = prname_lp(1:len_trim(prname_lp))//'vpvhvsvhrhogcgs.bin'
      open(unit=IIN,file=trim(filename),status='old',action='read',form='unformatted',iostat=ier)
      if (ier /= 0) then
        print *,'error opening file: ',trim(filename)
        stop 'error reading vpvhvsvhrhogcgs.bin file'
      endif
      read(IIN) vpv_read,vph_read,vsv_read,vsh_read,rho_read,gc_read,gs_read
      close(IIN)
      do ispec=1,nspec
        do k=1,NGLLZ
          do j=1,NGLLY
            do i=1,NGLLX
              call aniso_model_to_C21(vpv_read(i,j,k,ispec),vph_read(i,j,k,ispec),vsv_read(i,j,k,ispec),vsh_read(i,j,k,ispec),&
                                      rho_read(i,j,k,ispec),gc_read(i,j,k,ispec),gs_read(i,j,k,ispec),c11store(i,j,k,ispec), &
                                      c12store(i,j,k,ispec),c13store(i,j,k,ispec),c14store(i,j,k,ispec),c15store(i,j,k,ispec),&
                                      c16store(i,j,k,ispec),c22store(i,j,k,ispec),c23store(i,j,k,ispec),c24store(i,j,k,ispec),&
                                      c25store(i,j,k,ispec),c26store(i,j,k,ispec),c33store(i,j,k,ispec),c34store(i,j,k,ispec),&
                                      c35store(i,j,k,ispec),c36store(i,j,k,ispec),c44store(i,j,k,ispec),c45store(i,j,k,ispec),&
                                      c46store(i,j,k,ispec),c55store(i,j,k,ispec),c56store(i,j,k,ispec),c66store(i,j,k,ispec))
            enddo
          enddo
        enddo
      enddo
      !rhostore = rho_read
    else
      if (myrank == 0) write(IMAIN,*) '     reading in: c21.bin'
      filename = prname_lp(1:len_trim(prname_lp))//'c21.bin'
      open(unit=IIN,file=trim(filename),status='old',action='read',form='unformatted',iostat=ier)
      if (ier /= 0) then
        print *,'error opening file: ',trim(filename)
        stop 'error reading c21.bin file'
      endif
      read(IIN) c11_read,c12_read,c13_read,c14_read,c15_read,c16_read,c22_read,c23_read, &
                c24_read,c25_read,c26_read,c33_read,c34_read,c35_read,c36_read,c44_read, &
                c45_read,c46_read,c55_read,c56_read,c66_read,rho_read
      close(IIN)
      c11store = c11_read
      c12store = c12_read
      c13store = c13_read
      c14store = c14_read
      c15store = c15_read
      c16store = c16_read
      c22store = c22_read
      c23store = c23_read
      c24store = c24_read
      c25store = c25_read
      c26store = c26_read
      c33store = c33_read
      c34store = c34_read
      c35store = c35_read
      c36store = c36_read
      c44store = c44_read
      c45store = c45_read
      c46store = c46_read
      c55store = c55_read
      c56store = c56_read
      c66store = c66_read
      rhostore = rho_read
    endif
    ! user output
    if (myrank == 0) then
      write(IMAIN,*) ' GLL Aniso parameter check....by BinHe '
      write(IMAIN,*) ' max/min Gc :' ,maxval((c44store-c55store)/(c44store+c55store+1.0e-20)),&
                                      minval((c44store-c55store)/(c44store+c55store+1.0e-20))
      write(IMAIN,*) ' max/min Gs :' ,maxval((c45store+c45store)/(c44store+c55store+1.0e-20)),&
                                      minval((c45store+c45store)/(c44store+c55store+1.0e-20))
      write(IMAIN,*) ' max/min vpv :',sqrt(maxval((c11store+c22store)/rhostore*0.5)),&
                                      sqrt(maxval((c11store+c22store)/rhostore*0.5))
      write(IMAIN,*) ' max/min vsv :',sqrt(maxval((c44store+c55store)/rhostore*0.5)),&
                                      sqrt(maxval((c44store+c55store)/rhostore*0.5))
      write(IMAIN,*) ' max/min vph :',sqrt(maxval((c33store+c33store)/rhostore*0.5)),&
                                      sqrt(maxval((c33store+c33store)/rhostore*0.5))
      write(IMAIN,*) ' max/min vsh :',sqrt(maxval((c66store+c66store)/rhostore*0.5)),&
                                      sqrt(maxval((c66store+c66store)/rhostore*0.5))
      call flush_IMAIN()
    endif
    ! free memory
    deallocate(rho_read,vpv_read,vsv_read,vph_read,vsh_read,gc_read,gs_read)
    deallocate(c11_read,c12_read,c13_read,c14_read,c15_read,c16_read,c22_read,c23_read)
    deallocate(c24_read,c25_read,c26_read,c33_read,c34_read,c35_read,c36_read,c44_read)
    deallocate(c45_read,c46_read,c55_read,c56_read,c66_read)
    end subroutine model_gll_aniso

