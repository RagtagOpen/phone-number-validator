import phonenumbers
import phonenumbers.geocoder
import phonenumbers.carrier
import phonenumbers.timezone
from flask import jsonify, make_response, redirect, request
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


def validate_number(number):
    result = {"input": number}

    try:
        x = phonenumbers.parse(number, "US")

        reason_code = phonenumbers.is_possible_number_for_type_with_reason(
            x, phonenumbers.PhoneNumberType.PERSONAL_NUMBER
        )
        is_valid, reason_code = map_possible_reason.get(reason_code, (False, "unknown"))

        result["valid"] = is_valid
        result["reason"] = reason_code
    except phonenumbers.phonenumberutil.NumberParseException as e:
        result["valid"] = False
        result["reason"] = "invalid_format"
        result["message"] = str(e)

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


@numbers_bp.route("/v1/number/validate")
def parse_number():
    numbers = request.args.getlist("number")

    output = {"results": []}

    for number in numbers:
        output["results"].append(validate_number(number))

    return jsonify(output)


@numbers_bp.route("/favicon.ico")
def favicon_redirect():
    return redirect("https://assets.ragtag.tech/favicon.ico", 301)
