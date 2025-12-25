# app/coreAI/tools/destination_tools.py
import json
from typing import Optional, List
from langchain_core.tools import tool
from pydantic import BaseModel, Field

import dlog
from coreAI import embedding_service
from database.dao.milvus.destination_dao import DestinationDAO


class DestinationQuery(BaseModel):
    """Schema tìm kiếm điểm đến"""
    location: Optional[str] = Field(None, description="Tỉnh/thành phố (Đà Nẵng, Hà Nội, ...)")
    attraction_type: Optional[str] = Field(None, description="Loại (biển, núi, chùa, bảo tàng, ...)")
    activity: Optional[str] = Field(None, description="Hoạt động (tham quan, mạo hiểm, nghỉ dưỡng, ...)")
    keyword: Optional[str] = Field(None, description="Từ khóa tìm kiếm")
    price_range: Optional[str] = Field(None, description="Khoảng giá (free, <100k, 100-500k, >500k)")
    exclude_ids: Optional[List[str]] = Field(None, description="Loại trừ các ID đã hiển thị")


@tool(
    name_or_callable="retriever_destination_info",
    description="Tìm kiếm thông tin điểm đến du lịch dựa trên tiêu chí",
    args_schema=DestinationQuery
)
def retriever_destination_info_tool(
        location: Optional[str] = None,
        attraction_type: Optional[str] = None,
        activity: Optional[str] = None,
        keyword: Optional[str] = None,
        price_range: Optional[str] = None,
        exclude_ids: Optional[List[str]] = None
) -> str:
    """
    Tìm kiếm điểm đến du lịch

    Returns:
        JSON list các điểm đến: [{id, name, location, type, description, image_url, price_info}]
    """
    dlog.dlog_i(f"--- retriever_destination_info: location={location}, type={attraction_type}")

    # Tạo query text cho embedding
    query_parts = []
    if location:
        query_parts.append(f"location: {location}")
    if attraction_type:
        query_parts.append(f"type: {attraction_type}")
    if activity:
        query_parts.append(f"activity: {activity}")
    if keyword:
        query_parts.append(keyword)

    query_text = " ".join(query_parts) if query_parts else "điểm du lịch"

    # Tạo embedding
    query_vector = embedding_service.create_embedding(query_text)

    # Search trong database
    destination_dao = DestinationDAO()

    # Prepare filters
    filters = {}
    if price_range:
        filters["price_range"] = price_range
    if location:
        filters["location"] = location

    results = destination_dao.search_destinations(
        query_vector=query_vector,
        top_k=10,
        exclude_ids=exclude_ids or [],
        filters=filters
    )

    if not results:
        return json.dumps({
            "error": "Không tìm thấy điểm đến phù hợp",
            "suggestion": "Thử tìm kiếm với tiêu chí khác"
        }, ensure_ascii=False)

    # Format results
    formatted_results = []
    for dest in results:
        formatted_results.append({
            "id": dest.get("id"),
            "name": dest.get("name"),
            "location": dest.get("location"),
            "type": dest.get("attraction_type"),
            "description": dest.get("description"),
            "image_url": dest.get("image_url"),
            "thumbnail_url": dest.get("thumbnail_url"),
            "price_info": dest.get("price_info"),
            "rating": dest.get("rating"),
            "opening_hours": dest.get("opening_hours")
        })

    return json.dumps(formatted_results, ensure_ascii=False, indent=2)


@tool(name_or_callable="get_destination_details")
def get_destination_details_tool(destination_id: str) -> str:
    """
    Lấy thông tin chi tiết của một điểm đến cụ thể

    Args:
        destination_id: ID của điểm đến

    Returns:
        JSON với đầy đủ thông tin điểm đến
    """
    dlog.dlog_i(f"--- get_destination_details: {destination_id}")

    destination_dao = DestinationDAO()
    destination = destination_dao.get_destination_by_id(destination_id)

    if not destination:
        return json.dumps({
            "error": f"Không tìm thấy điểm đến với ID: {destination_id}"
        }, ensure_ascii=False)

    return json.dumps(destination, ensure_ascii=False, indent=2)


@tool(name_or_callable="get_nearby_attractions")
def get_nearby_attractions_tool(destination_id: str, radius_km: float = 10.0) -> str:
    """
    Tìm các điểm tham quan gần một địa điểm

    Args:
        destination_id: ID điểm đến trung tâm
        radius_km: Bán kính tìm kiếm (km)

    Returns:
        JSON list các điểm gần
    """
    dlog.dlog_i(f"--- get_nearby_attractions: {destination_id}, radius={radius_km}km")

    destination_dao = DestinationDAO()
    nearby = destination_dao.get_nearby_destinations(destination_id, radius_km)

    if not nearby:
        return json.dumps({
            "message": "Không tìm thấy điểm tham quan gần",
            "results": []
        }, ensure_ascii=False)

    return json.dumps({"results": nearby}, ensure_ascii=False, indent=2)


@tool(name_or_callable="get_events_and_festivals")
def get_events_and_festivals_tool(location: str, month: Optional[int] = None) -> str:
    """
    Lấy thông tin sự kiện, lễ hội tại địa phương

    Args:
        location: Tên địa phương
        month: Tháng (1-12), None = tất cả

    Returns:
        JSON list sự kiện/lễ hội
    """
    dlog.dlog_i(f"--- get_events_and_festivals: {location}, month={month}")

    destination_dao = DestinationDAO()
    events = destination_dao.get_events_by_location(location, month)

    if not events:
        return json.dumps({
            "message": f"Không có sự kiện/lễ hội tại {location}" + (f" trong tháng {month}" if month else ""),
            "results": []
        }, ensure_ascii=False)

    return json.dumps({"results": events}, ensure_ascii=False, indent=2)