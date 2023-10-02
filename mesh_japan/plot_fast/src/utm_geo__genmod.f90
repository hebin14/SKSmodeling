        !COMPILER-GENERATED INTERFACE MODULE: Sun Oct  1 23:14:12 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE UTM_GEO__genmod
          INTERFACE 
            SUBROUTINE UTM_GEO(RLON4,RLAT4,RX4,RY4,UTM_PROJECTION_ZONE, &
     &IWAY)
              REAL(KIND=8), INTENT(INOUT) :: RLON4
              REAL(KIND=8), INTENT(INOUT) :: RLAT4
              REAL(KIND=8), INTENT(INOUT) :: RX4
              REAL(KIND=8), INTENT(INOUT) :: RY4
              INTEGER(KIND=4), INTENT(IN) :: UTM_PROJECTION_ZONE
              INTEGER(KIND=4), INTENT(IN) :: IWAY
            END SUBROUTINE UTM_GEO
          END INTERFACE 
        END MODULE UTM_GEO__genmod
