/* © 2026 Andrei Levin - Codebeex srl (www.codebeex.com)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 *
 * Fix for hr_attendance_geolocation (OCA/hr).
 *
 * In the original module, when the browser denies location access, has no
 * geolocation API, or the request times out (5s), getCurrentPosition() calls
 * the error callback which only does a console.warn(). The attendance RPC is
 * never sent, so pressing "Check in / Check out" silently does nothing.
 *
 * Two problems are fixed here:
 *   1. The error callback was passed UNBOUND (`self._getPositionError`), so
 *      `this` was lost inside it and it could not do any real work anyway.
 *      We rebind it and also cover the "no geolocation API" branch.
 *   2. On any location failure we now still record the attendance, just
 *      WITHOUT coordinates (location = false). The Python side
 *      (hr.employee.attendance_action_change) already skips writing the
 *      lat/long when location is falsy, so no server change is required.
 */
odoo.define('hr_attendance_geolocation_fix.attendances_geolocation_fix', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var KioskConfirm = require('hr_attendance.kiosk_confirm');

    var GEO_OPTIONS = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
    };

    // Extract [latitude, longitude] from a Geolocation position, or `false`
    // when no usable position is available (so the server skips the coords).
    function _locationFromPosition(position) {
        if (position && position.coords) {
            return [position.coords.latitude, position.coords.longitude];
        }
        return false;
    }

    function _requestPosition(widget) {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                widget._manual_attendance.bind(widget),
                widget._getPositionError.bind(widget),  // rebind: original lost `this`
                GEO_OPTIONS
            );
        } else {
            // No geolocation API at all -> record attendance without coords.
            widget._manual_attendance();
        }
    }

    MyAttendances.include({
        update_attendance: function () {
            _requestPosition(this);
        },
        _manual_attendance: function (position) {
            var self = this;
            var location = _locationFromPosition(position);
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', null, location],
            })
            .then(function (result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
                }
            });
        },
        _getPositionError: function (error) {
            console.warn(
                'hr_attendance_geolocation_fix: location unavailable (' +
                error.code + '): ' + error.message +
                ' - recording attendance without coordinates.'
            );
            this._manual_attendance();
        },
    });

    KioskConfirm.include({
        update_attendance: function () {
            _requestPosition(this);
        },
        _manual_attendance: function (position) {
            var self = this;
            var location = _locationFromPosition(position);
            if (this.pin_pad) {
                this.$('.o_hr_attendance_pin_pad_button_ok').attr("disabled", "disabled");
            }
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[this.employee_id], this.next_action, this.$('.o_hr_attendance_PINbox').val(), location],
            })
            .then(function (result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
                    if (self.pin_pad) {
                        self.$('.o_hr_attendance_PINbox').val('');
                        setTimeout(function () {
                            self.$('.o_hr_attendance_pin_pad_button_ok').removeAttr("disabled");
                        }, 500);
                    }
                    self.pin_pad = false;
                }
            });
        },
        _getPositionError: function (error) {
            console.warn(
                'hr_attendance_geolocation_fix: location unavailable (' +
                error.code + '): ' + error.message +
                ' - recording attendance without coordinates.'
            );
            this._manual_attendance();
        },
    });

});
