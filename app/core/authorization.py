from fastapi import status
from app.exceptions.custom_exception import AppException


async def get_property_owned_by_user(property_model, property_id, user_id):
    property = await property_model.filter(id=property_id, owner_id=user_id).first()
    if not property:
        raise AppException("Property not found", status.HTTP_404_NOT_FOUND)
    return property


async def get_unit_owned_by_user(unit_model, unit_id, user_id):
    unit = await unit_model.filter(id=unit_id, property__owner_id=user_id).first()
    if not unit:
        raise AppException("Unit not found", status.HTTP_404_NOT_FOUND)
    return unit


async def get_tenant_owned_by_user(tenant_model, tenant_id, user_id):
    tenant = await tenant_model.filter(
        id=tenant_id, user_id=user_id, is_active=True
    ).first()
    if not tenant:
        raise AppException("Tenant not found", status.HTTP_404_NOT_FOUND)
    return tenant


async def get_payment_owned_by_user(payment_model, payment_id, user_id):
    payment = await payment_model.filter(
        id=payment_id, user_id=user_id, is_reversed=False
    ).first()
    if not payment:
        raise AppException("Payment not found", status.HTTP_404_NOT_FOUND)
    return payment


async def get_document_owned_by_user(document_model, document_id, user_id):
    document = await document_model.filter(
        id=document_id, tenant__user_id=user_id
    ).first()
    if not document:
        raise AppException("Document not found", status.HTTP_404_NOT_FOUND)
    return document


async def get_expense_owned_by_user(expense_model, expense_id, user_id):
    expense = await expense_model.filter(id=expense_id, user_id=user_id).first()
    if not expense:
        raise AppException("Expense not found", status.HTTP_404_NOT_FOUND)
    return expense
