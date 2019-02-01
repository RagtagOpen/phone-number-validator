import phonenumbers
import phonenumbers.geocoder
import phonenumbers.carrier
import phonenumbers.timezone
from flask import abort, jsonify, make_response
from phonescrubber.numbers import numbers_bp


map_possible_reason = {
    phonenumbers.ValidationResult.IS_POSSIBLE: (True, "possible"),
    phonenumbers.ValidationResult.IS_POSSIBLE_LOCAL_ONLY: (True, "possible_local"),
    phonenumbers.ValidationResult.INVALID_COUNTRY_CODE: (False, "invalid_country_code"),
    phonenumbers.ValidationResult.TOO_SHORT: (False, "too_short"),
    phonenumbers.ValidationResult.INVALID_LENGTH: (False, "invalid_length"),
    phonenumbers.ValidationResult.TOO_LONG: (False, "too_long"),
}

map_phone_type = {
    phonenumbers.PhoneNumberType.FIXED_LINE: "fixed_line",
    phonenumbers.PhoneNumberType.MOBILE: "mobile",
    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "fixed_or_mobile",
    phonenumbers.PhoneNumberType.TOLL_FREE: "toll_free",
    phonenumbers.PhoneNumberType.PREMIUM_RATE: "premium_rate",
    phonenumbers.PhoneNumberType.SHARED_COST: "shared_cost",
    phonenumbers.PhoneNumberType.VOIP: "voip",
    phonenumbers.PhoneNumberType.PERSONAL_NUMBER: "personal_number",
    phonenumbers.PhoneNumberType.PAGER: "pager",
    phonenumbers.PhoneNumberType.UAN: "uan",
    phonenumbers.PhoneNumberType.VOICEMAIL: "voicemail",
    phonenumbers.PhoneNumberType.UNKNOWN: "unknown",
}


@numbers_bp.route("/v1/number/<telephone>")
def check_number(telephone):
    try:
        x = phonenumbers.parse(telephone, "US")
    except phonenumbers.phonenumberutil.NumberParseException as e:
        resp = jsonify({"valid": False, "reason": "invalid_format", "message": str(e)})
        resp.status_code = 400
        return resp

    reason_code = phonenumbers.is_possible_number_for_type_with_reason(
        x, phonenumbers.PhoneNumberType.PERSONAL_NUMBER
    )
    is_valid, reason_code = map_possible_reason.get(reason_code, (False, "unknown"))

    result = {"valid": is_valid, "reason": reason_code}

    if result["valid"]:
        result["formatted"] = {
            "e164": phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164),
            "national": phonenumbers.format_number(
                x, phonenumbers.PhoneNumberFormat.NATIONAL
            ),
        }

        type_code = phonenumbers.number_type(x)
        result["type"] = map_phone_type.get(type_code, "unknown")

        result["location"] = {
            "description": phonenumbers.geocoder.description_for_number(x, "en"),
            "tz": phonenumbers.timezone.time_zones_for_number(x),
        }

    return jsonify(result)
