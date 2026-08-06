from fastapi import APIRouter, Depends
from uuid import UUID

from app.core.response import ApiResponse

from app.platform.auth.dependencies import get_current_tenant
from app.platform.mail.json_repository import JsonMailRepository
from app.platform.mail.service import MailService

from app.platform.mail.schemas import *

router = APIRouter(
    prefix="/mail",
    tags=["Mail Automation"],
)


def get_service(
    tenant=Depends(get_current_tenant),
):

    repo = JsonMailRepository(
        tenant.uuid,
    )

    return MailService(repo)

@router.get("/dashboard")
def dashboard(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.dashboard()
    )


@router.get("/customers")
def customers(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.get_customers()
    )


@router.post("/customers")
def create_customer(
    data: CustomerCreate,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=service.create_customer(data)
    )


@router.put("/customers/{customer_uuid}")
def update_customer(
    customer_uuid: UUID,
    data: CustomerUpdate,
    service: MailService = Depends(get_service)
):

    return ApiResponse.ok(
        data=service.update_customer(
            customer_uuid,
            data,
        )
    )


@router.delete("/customers/{customer_uuid}")
def delete_customer(
    customer_uuid: UUID,
    service: MailService = Depends(get_service)
):

    service.delete_customer(customer_uuid)

    return ApiResponse.ok(
        message="Customer deleted"
    )


@router.get("/products")
def products(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.get_products()
    )


@router.post("/products")
def create_product(
    data: ProductCreate,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=service.get_products()
    )


@router.put("/products/{product_uuid}")
def update_product(
    product_uuid: UUID,
    data: ProductUpdate,
    service: MailService = Depends(get_service)
):

    return ApiResponse.ok(
        data=service.update_product(
            product_uuid,
            data,
        )
    )


@router.delete("/products/{product_uuid}")
def delete_product(
    product_uuid: UUID,
    service: MailService = Depends(get_service)
):
    service.delete_product(product_uuid)

    return ApiResponse.ok(
        message="Product deleted"
    )



@router.get("/orders")
def orders(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.get_orders()
    )

@router.get("/orders/{order_uuid}")
def order(
    order_uuid: UUID,
    service: MailService = Depends(get_service),
):

    return ApiResponse.ok(
        data=service.get_order(order_uuid)
    )


@router.post("/orders")
def create_order(
    data: OrderCreate,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=service.create_order(data)
    )


@router.put("/orders/{order_uuid}")
def update_order(
    order_uuid: UUID,
    data: OrderUpdate,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=service.update_order(
            order_uuid,
            data,
        )
    )


@router.delete("/orders/{order_uuid}")
def delete_order(
    order_uuid: UUID,
    service: MailService = Depends(get_service)
):
    service.delete_order(order_uuid)

    return ApiResponse.ok(
        message="Order deleted"
    )


# =====================================================
# ORDER ACTIONS
# =====================================================

@router.put("/orders/{order_uuid}/address")
def update_address(
    order_uuid: UUID,
    data: AddressUpdateRequest,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=service.update_address(order_uuid, data)
    )


@router.post("/orders/{order_uuid}/track")
def track_order(
    order_uuid: UUID,
    data: TrackingRequest,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=repository.track_order(order_uuid, data)
    )


@router.post("/orders/{order_uuid}/cancel")
def cancel_order(
    order_uuid: UUID,
    data: CancelRequest,
    service: MailService = Depends(get_service)
):
    
    return ApiResponse.ok(
        data=service.cancel_order(order_uuid, data)
    )


@router.post("/orders/{order_uuid}/return")
def return_order(
    order_uuid: UUID,
    data: ReturnRequest,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.return_order(order_uuid, data)
    )


@router.post("/orders/{order_uuid}/replacement")
def replacement_order(
    order_uuid: UUID,
    data: ReplacementRequest,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.replacement_order(order_uuid, data)
    )


@router.post("/orders/{order_uuid}/refund")
def refund_order(
    order_uuid: UUID,
    data: RefundRequest,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.refund_order(order_uuid, data)
    )


@router.get("/orders/{order_uuid}/invoice")
def invoice(
    order_uuid: UUID,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.generate_invoice(order_uuid)
    )


# =====================================================
# TICKETS
# =====================================================

@router.get("/tickets")
def tickets(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.get_tickets()
    )


@router.post("/tickets")
def create_ticket(
    data: TicketCreate,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.create_ticket(data)
    )


@router.put("/tickets/{ticket_uuid}")
def update_ticket(
    ticket_uuid: UUID,
    data: TicketUpdate,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.update_ticket(ticket_uuid, data)
    )


# =====================================================
# CONVERSATIONS
# =====================================================

@router.get("/conversations")
def conversations(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.get_conversations()
    )


@router.post("/conversations")
def create_conversation(
    data: ConversationCreate,
    service: MailService = Depends(get_service)
):
    return ApiResponse.ok(
        data=service.create_conversation(data)
    )


@router.post("/conversations/{conversation_uuid}/messages")
def add_message(
    conversation_uuid: UUID,
    data: MessageCreate,
    service: MailService = Depends(get_service)
):
      
    return ApiResponse.ok(
        data=service.add_message(
            conversation_uuid,
            data,
        )
    )


# =====================================================
# EMAIL LOGS
# =====================================================
@router.get("/email-logs")
def email_logs(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.get_email_logs()
    )

# =====================================================
# HEALTH CHECK
# =====================================================
@router.get("/health")
def health(
    service: MailService = Depends(get_service),
):
    return ApiResponse.success(
        data=service.ping()
    )

@router.post(
    "/test-email",
    response_model=TestEmailResponse,
)
def process_test_email(
    request: TestEmailRequest,
    service: MailService = Depends(get_service),
):
    return service.process_test_email(request)