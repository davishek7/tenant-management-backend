from enum import Enum


class LedgerEntryType(str, Enum):
    RENT = "RENT"
    PAYMENT = "PAYMENT"
    UTILITY = "UTILITY"
    ADJUSTMENT = "ADJUSTMENT"


class PaymentMode(str, Enum):
    CASH = "CASH"
    UPI = "UPI"
    BANK = "BANK"


class UtilityType(str, Enum):
    ELECTRICITY = "ELECTRICITY"
    WATER = "WATER"
    GAS = "GAS"
    INTERNET = "INTERNET"
    MAINTENANCE = "MAINTENANCE"


class AdjustmentReason(str, Enum):
    LATE_FEE = "LATE_FEE"
    DISCOUNT = "DISCOUNT"
    WAIVER = "WAIVER"
    CORRECTION = "CORRECTION"
    OTHER = "OTHER"


class TenantDocType(str, Enum):
    ID_PROOF = "ID_PROOF"
    ADDRESS_PROOF = "ADDRESS_PROOF"
    RENT_AGREEMENT = "RENT_AGREEMENT"
    POLICE_VERIFICATION = "POLICE_VERIFICATION"
    PROFILE_PHOTO = "PROFILE_PHOTO"
    EMPLOYMENT_PROOF = "EMPLOYMENT_PROOF"
    OTHER = "OTHER"
