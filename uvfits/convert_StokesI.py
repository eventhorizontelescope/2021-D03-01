#!/usr/bin/env python3
#
# Copyright (C) 2019 The Event Horizon Telescope Collaboration
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import ehtim as eh

doy = {'3600':'100'}

path0='../orig-uvfits/'

for obs in ['e17a10hi','e17a10lo']:
    for pipe in ['casa', 'hops']:
        pathf=path0+'{0}_{1}_CENA_netcal.uvfits'.format(pipe, obs)
        if not os.path.isfile(pathf):
            continue

        f0stokes = eh.obsdata.load_uvfits(pathf,polrep='stokes')
        for col in ['qvis','uvis','vvis','qsigma','usigma']:
            #remove non-Stokes I components but keep Stokes V errors for consistent
            #treatment of errors magnitude with Stokes / pseudo Stokes data present
            f0stokes.data[col] *= 0 # this operation is nan-preserving

        # remove record of single polarization pseudo-I construction (remove nan)
        f0stokes.data['vvis'] = 0. * f0stokes.data['vis']
        f0stokes.data['vsigma'] = 1. * f0stokes.data['sigma']

        outname='CenA_2017_100_{0}_{1}_netcal_StokesI.uvfits'.format(obs[-2:], pipe)
        f0stokes.save_uvfits('uvfits/'+outname)
