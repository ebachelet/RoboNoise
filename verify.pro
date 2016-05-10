PRO verify

;Program to verify the results coming from Etienne's implementation by using "fit_photometric_calibration.pro"
;on EXACTLY the same data
filename = 'Dan.Data.OB141185.txt'
;filename = 'Dan.Data.OB13446.txt'

;Read in data file
print, ''
print, 'Reading in data file...'
if (filename EQ 'Dan.Data.OB141185.txt') then begin
  read_data_columns_from_ascii_file, filename, 0, -1, [1,2,3,15,16,17,18,19,20,22,23], ['s','s','d','d','d','d','d','d','d','d','d'], ndata, status, errstr, $
                                     stars, frames, hjd, mag, merr, exp, bkgd, seeing, ps, ccdx, ccdy
endif else begin
  read_data_columns_from_ascii_file, filename, 0, -1, [1,2,3,15,16,17,18,19,20,22,23], ['s','s','d','d','d','d','d','d','d','d','d'], ndata, status, errstr, $
                                     stars, frames, hjd, mag, merr, exp, bkgd, seeing, ps, ccdx, ccdy
endelse

;Call "fit_photometric_calibration.pro"
danidl_cppcode = '/home/dbramich/IDL/DanIDL/C++.Code'
fit_options = {fit_zp : 'group', fit_ext : 'no', fit_nonlin_ext : 0, fit_col : 0, fit_air_col : 'no', fit_illcorr : 0, fit_q1 : 0, fit_q2 : 0, fit_q3q4 : 0, $
               fit_patt : 'no'} 
fit_photometric_calibration, mag, merr, stars, 'lc_00023.687_00224.673_t', 18.95, std_star_colour, airmass, ccdx, ccdy, seeing, ps, q3, q4, patt_arr, $
                             frames, group_id_ext, fit_options, fit_params, model, chisq, status, danidl_cppcode, /ERRBAR

;print, fit_params.npar
;print, fit_params.nstars



END
