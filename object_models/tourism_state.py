# app/object_models/tourism_state.py
from typing import TypedDict, List, Optional, Annotated
from datetime import datetime
import operator


class TourismState(TypedDict):
    """State quản lý hội thoại du lịch"""

    # Message history
    messages: Annotated[List, operator.add]
    human_message: str
    ai_message: str

    # Agent tracking
    current_agent: str
    next_agent: str

    # User info
    thread_id: str
    customer: int
    customer_location: Optional[str]
    customer_language: str  # vi, en, ...

    # Destination info
    destination_query: Optional[str]
    selected_destination: Optional[str]
    destination_details: Optional[dict]

    # Itinerary planning
    itinerary_info: Optional[dict]  # {destination, duration, budget, preferences, travel_date}
    suggested_itinerary: Optional[dict]

    # Booking info
    booking_info: Optional[dict]  # {service_type, details, customer_info, booking_id}

    # Weather & emergency
    weather_info: Optional[dict]
    emergency_contacts: Optional[List[dict]]

    # System
    documents: Optional[List[dict]]
    grader_status: Optional[str]
    agent_status: Optional[str]


class DestinationQuery(BaseModel):
    """Schema tìm kiếm điểm đến"""
    location: Optional[str] = Field(None, description="Địa điểm (Đà Nẵng, Hà Nội, ...)")
    attraction_type: Optional[str] = Field(None, description="Loại điểm tham quan (bãi biển, núi, chùa, ...)")
    activity: Optional[str] = Field(None, description="Hoạt động (tham quan, mạo hiểm, nghỉ dưỡng, ...)")
    price_range: Optional[str] = Field(None, description="Khoảng giá vé")
    season: Optional[str] = Field(None, description="Mùa thích hợp")


class ItineraryRequest(BaseModel):
    """Schema yêu cầu lịch trình"""
    destination: str = Field(..., description="Điểm đến")
    duration: int = Field(..., description="Số ngày", ge=1, le=30)
    start_date: str = Field(..., description="Ngày bắt đầu (YYYY-MM-DD)")
    number_of_people: int = Field(1, description="Số người", ge=1)
    budget: Optional[float] = Field(None, description="Ngân sách (VNĐ)")
    preferences: Optional[List[str]] = Field(None, description="Sở thích [ẩm thực, lịch sử, mạo hiểm, nghỉ dưỡng]")
    accommodation_type: Optional[str] = Field(None, description="Loại chỗ ở (khách sạn, homestay, resort)")
    transportation: Optional[str] = Field(None, description="Phương tiện (máy bay, xe, tàu)")


class BookingRequest(BaseModel):
    """Schema đặt dịch vụ"""
    service_type: str = Field(..., description="Loại dịch vụ (tour, hotel, flight, attraction)")
    service_id: Optional[str] = Field(None, description="Mã dịch vụ")
    check_in: str = Field(..., description="Ngày nhận/check-in (YYYY-MM-DD)")
    check_out: Optional[str] = Field(None, description="Ngày trả/check-out (YYYY-MM-DD)")
    number_of_people: int = Field(..., description="Số người", ge=1)

    # Customer info
    customer_name: str = Field(..., description="Tên khách hàng")
    customer_phone: str = Field(..., description="Số điện thoại")
    customer_email: Optional[str] = Field(None, description="Email")

    # Additional info
    special_requests: Optional[str] = Field(None, description="Yêu cầu đặc biệt")
    payment_method: Optional[str] = Field(None, description="Phương thức thanh toán")


class WeatherQuery(BaseModel):
    """Schema tra cứu thời tiết"""
    location: str = Field(..., description="Địa điểm")
    date: Optional[str] = Field(None, description="Ngày cần xem thời tiết (YYYY-MM-DD)")
    days: Optional[int] = Field(7, description="Số ngày dự báo", ge=1, le=14)


from pydantic import BaseModel, Field