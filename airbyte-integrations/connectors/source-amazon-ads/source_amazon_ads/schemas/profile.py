#
# MIT License
#
# Copyright (c) 2020 Airbyte
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from decimal import Decimal

from .common import JSEnum, JSModel


class CountryCodes(JSEnum):
    US = "US"
    CA = "CA"
    MX = "MX"
    BR = "BR"
    UK = "UK"
    DE = "DE"
    FR = "FR"
    ES = "ES"
    IT = "IT"
    NL = "NL"
    JP = "JP"
    AU = "AU"
    AE = "AE"
    SG = "SG"


class CurrencyCodes(JSEnum):
    USD = "USD"
    CAD = "CAD"
    MXN = "MXN"
    BRL = "BRL"
    GBP = "GBP"
    JPY = "JPY"
    EUR = "EUR"
    AUD = "AUD"
    AED = "AED"


class TimeZones(JSEnum):
    AMERICA_LOS_ANGELES = "America/Los_Angeles"
    AMERICA_SAO_PAULO = "America/Sao_Paulo"
    EUROPE_LONDON = "Europe/London"
    EUROPE_PARIS = "Europe/Paris"
    ASIA_TOKYO = "Asia/Tokyo"
    AUSTRALIA_SYDNEY = "Australia/Sydney"
    ASIA_DUBAI = "Asia/Dubai"
    ASIA_SINGAPORE = "Asia/Singapore"


class Types(JSEnum):
    VENDOR = "vendor"
    SELLER = "seller"
    AGENCY = "agency"


class SubTypes(JSEnum):
    KDP_AUTHOR = "KDP_AUTHOR"
    AMAZON_ATTRIBUTION = "AMAZON_ATTRIBUTION"


class AccountInfo(JSModel):
    marketplaceStringId: str
    id: str
    type: Types
    name: str = None
    subType: SubTypes = None
    validPaymentMethod: bool = None


class Profile(JSModel):
    profileId: int
    countryCode: CountryCodes = None
    currencyCode: CurrencyCodes = None
    dailyBudget: Decimal = None
    timezone: TimeZones
    accountInfo: AccountInfo
