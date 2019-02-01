import phonenumbers
import phonenumbers.geocoder
import phonenumbers.carrier
import phonenumbers.timezone
from flask import abort, jsonify, make_response
from phonescrubber.numbers import numbers_bp


@numbers_bp.route("/v1/number/<telephone>")
def check_number(telephone):
    try:
        x = phonenumbers.parse(telephone, "US")
    except phonenumbers.phonenumberutil.NumberParseException as e:
        resp = jsonify({"msg": "Invalid format: %s" % e})
        resp.status_code = 400
        return resp

    return jsonify(
        {
            "result": "ok",
            "formats": {
                "e164": phonenumbers.format_number(
                    x, phonenumbers.PhoneNumberFormat.E164
                ),
                "national": phonenumbers.format_number(
                    x, phonenumbers.PhoneNumberFormat.NATIONAL
                ),
            },
            "location": phonenumbers.geocoder.description_for_number(x, "en"),
            "tz": phonenumbers.timezone.time_zones_for_number(x),
        }
    )
