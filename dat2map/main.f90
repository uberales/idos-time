! Creates a map of reachability of a specified public transport 
! stop (pivot stop) from all locations on 2D grid. 
! 
! Takes a few coordinate points with specified reachability, 
! creates minimal rectangle and covers it with n x m grid, 
! where n is specified at input and m is calculated using 
! the rectangle's aspect ratio. The time of travel from 
! arbitrary point to the pivot stop is calculated as the 
! minimum of all times needed to walk a straight line + time 
! of travel from the available stops.
! 
! Time complexity of the algorithm is O(n^2 * s), which is 
! poor. But the Fortran implementation makes it bearable 
! enough to produce grids 4096 points wide.
! 
! Input: list of travel times to specified coordinates, horizontal resolution.
! Output: 2D map of the reachabilities (and stops, if specified)

program idos
    use getoptions

    implicit none

    character :: okey
    character(len=512) :: input_file='arrivals_final-fortran.dat'//char(0), output_file='time_map.map'//char(0), stops_file='stops_map.map'//char(0)
    real*8, dimension(:), allocatable :: stop_lat, stop_lon, stop_time
    real*8 :: lat, lon, time
    real*8 :: min_lat, min_lon, max_lat, max_lon, delta_lat, delta_lon, step_lat, step_lon, min_t, att_t
    integer :: res_lat, res_lon
    integer :: stop_count, i, i_lat, i_lon, i_stop
    real*8, dimension(:,:), allocatable :: time_map
    integer*8, dimension(:,:), allocatable :: stops_map
    logical :: draw_stops

    real*8 :: walking_time

    draw_stops = .false.
    res_lon = 256

    write(*,*) 'Parsing command line'

    do
        okey=getopt('i:o:r:s:')
        if(okey.eq.'>') exit
        if(okey.eq.'!') then
            write(6,*) 'Unknown option: ', trim(optarg)
            stop
        end if

        if(okey.eq.'o') then
            output_file = trim(optarg)
            write(6,*) 'Output file: ', trim(optarg)
        end if

        if(okey.eq.'i') then
            input_file = trim(optarg)
            write(6,*) 'Input file: ', trim(optarg)
        end if

        if(okey.eq.'s') then
            stops_file = trim(optarg)
            draw_stops = .true.
            write(6,*) 'Stops file: ', trim(optarg)
        end if

        if(okey.eq.'r') then
            read(optarg, '(i)') res_lon
            write(6,*) 'Horizontal resolution: ', res_lon
        end if

    end do

    stop_count = 0
    open(unit = 2, file = input_file)
    read(2,*) stop_count

    allocate(stop_lat(stop_count))
    allocate(stop_lon(stop_count))
    allocate(stop_time(stop_count))

    do i = 1, stop_count
        read(2,*) stop_lat(i), stop_lon(i), stop_time(i)
    enddo

    close(2)

    min_lat = minval(stop_lat)
    min_lon = minval(stop_lon)

    max_lat = maxval(stop_lat)
    max_lon = maxval(stop_lon)

    delta_lat = max_lat - min_lat
    delta_lon = max_lon - min_lon

    res_lat = int(ceiling(delta_lat * (res_lon - 1) / delta_lon))

    step_lon = delta_lon / res_lon
    step_lat = delta_lat / res_lat

    write(*,*) "Dim size: ", delta_lat, delta_lon
    write(*,*) "Step size: ", step_lat, step_lon
    write(*,*) "Image size: ", res_lat, res_lon

    allocate(time_map(res_lat, res_lon))

    lat = min_lat
    do i_lat = 1, res_lat
        lon = min_lon
        do i_lon = 1, res_lon
            min_t = 0.0
            do i_stop = 1, stop_count
                att_t = walking_time(lat, lon, stop_lat(i_stop), stop_lon(i_stop)) + stop_time(i_stop)
                if (i_stop == 1 .or. att_t < min_t) then
                    min_t = att_t
                endif
            enddo
            !         map_data[res_lat - (i_lat + 1)][i_lon] = t
            time_map(res_lat - i_lat + 1, i_lon) = min_t
            lon = lon + step_lon
        enddo

        write(*,*) 'Latitude done', i_lat
        lat = lat + step_lat
    enddo

    open(unit = 2, file = output_file, status="replace", action="write")
    write(2, *) min_lat, min_lon
    write(2, *) max_lat, max_lon
    do i_lat = 1, res_lat
        do i_lon = 1, res_lon
            write(2, '(F)', advance='no') time_map(i_lat, i_lon)
        end do
        write(2, '(A/)', advance='no') ''
    end do
    close(2)

    if (draw_stops) then
        allocate(stops_map(res_lat, res_lon))
        stops_map = 0
        do i = 1, stop_count
            i_lat = int(floor((stop_lat(i) - min_lat) / step_lat)) + 1
            i_lon = int(floor((stop_lon(i) - min_lon) / step_lon)) + 1

            if (i_lat > res_lat) then
                i_lat = res_lat
            endif

            if (i_lon > res_lon) then
                i_lon = res_lon
            endif

            write(*,*) 'stop at ', i_lat, i_lon
            stops_map(res_lat - i_lat + 1, i_lon) = stops_map(i_lat, i_lon) + 1
        enddo

        open(unit = 2, file = stops_file, status="replace", action="write")
        write(2, *) min_lat, min_lon
        write(2, *) max_lat, max_lon
        do i_lat = 1, res_lat
            do i_lon = 1, res_lon
                write(2, '(I)', advance='no') stops_map(i_lat, i_lon)
            end do
            write(2, '(A/)', advance='no') ''
        end do
        close(2)

        deallocate(stops_map)
    endif

    deallocate(time_map)

    deallocate(stop_lat)
    deallocate(stop_lon)
    deallocate(stop_time)

end program


function radians(degrees)
    real*8 :: radians
    real*8 :: degrees, pi
    pi = 3.1415926535
    radians = pi * degrees / 180.0
end function


function walking_time(a_lat, a_lon, b_lat, b_lon)
    implicit none
    real*8 :: walking_time
    real*8 :: a_lat, a_lon, b_lat, b_lon
    real*8 :: a_phi, b_phi, delta_phi, delta_lambda, a, c, R, d, v

    real*8 :: radians

    walking_time = 0.0
    R = 6378000.0
    v = 70.0 ! m/min

    a_phi = radians(a_lat)
    b_phi = radians(b_lat)
    delta_phi = radians(b_lat - a_lat)
    delta_lambda = radians(b_lon - a_lon)

    a = sin(0.5 * delta_phi) * sin(0.5 * delta_phi) + cos(a_phi) * cos(b_phi) * sin(0.5 * delta_lambda) * sin(0.5 * delta_lambda)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c

    walking_time = d / v
end function
