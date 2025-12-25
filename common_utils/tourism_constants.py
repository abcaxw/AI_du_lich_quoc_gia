# app/common_utils/tourism_constants.py

# Danh sách tỉnh/thành phố du lịch Việt Nam
VN_TOURISM_CITIES = [
    "Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Nha Trang", "Hội An",
    "Huế", "Hạ Long", "Sapa", "Đà Lạt", "Phú Quốc",
    "Hải Phòng", "Cần Thơ", "Vũng Tàu", "Phan Thiết", "Quy Nhơn",
    "Ninh Bình", "Mai Châu", "Mù Cang Chải", "Cao Bằng", "Hà Giang"
]

# Loại điểm tham quan
ATTRACTION_TYPES = {
    "beach": ["bãi biển", "biển", "beach", "seaside"],
    "mountain": ["núi", "đồi", "mountain", "hill"],
    "temple": ["chùa", "đền", "miếu", "temple", "pagoda", "shrine"],
    "museum": ["bảo tàng", "museum"],
    "historical": ["di tích lịch sử", "lịch sử", "historical site"],
    "nature": ["thiên nhiên", "vườn quốc gia", "nature", "national park"],
    "entertainment": ["vui chơi giải trí", "công viên", "entertainment", "theme park"],
    "cave": ["hang động", "cave", "grotto"],
    "waterfall": ["thác", "waterfall"],
    "market": ["chợ", "market"],
    "architecture": ["kiến trúc", "architecture", "landmark"]
}

# Hoạt động du lịch
ACTIVITY_TYPES = {
    "sightseeing": ["tham quan", "ngắm cảnh", "sightseeing"],
    "adventure": ["mạo hiểm", "thám hiểm", "adventure", "trekking", "hiking"],
    "relaxation": ["nghỉ dưỡng", "thư giãn", "relaxation", "spa", "resort"],
    "culture": ["văn hóa", "lịch sử", "culture", "cultural"],
    "food": ["ẩm thực", "món ăn", "food", "cuisine"],
    "shopping": ["mua sắm", "shopping"],
    "water_sports": ["thể thao nước", "lặn biển", "water sports", "diving", "snorkeling"],
    "photography": ["chụp ảnh", "photography"]
}

# Sở thích du lịch
TRAVEL_PREFERENCES = {
    "food_lover": ["ẩm thực", "food", "cuisine", "eating"],
    "history_buff": ["lịch sử", "history", "historical"],
    "adventure_seeker": ["mạo hiểm", "adventure", "extreme"],
    "nature_lover": ["thiên nhiên", "nature", "eco"],
    "beach_lover": ["biển", "beach", "seaside"],
    "culture_enthusiast": ["văn hóa", "culture", "traditional"],
    "photography": ["chụp ảnh", "photography", "photo"],
    "relaxation": ["nghỉ dưỡng", "relaxation", "spa"]
}

# Khoảng giá vé
PRICE_RANGES = {
    "free": {"min": 0, "max": 0, "label": "Miễn phí"},
    "cheap": {"min": 0, "max": 100000, "label": "Dưới 100k"},
    "medium": {"min": 100000, "max": 500000, "label": "100k - 500k"},
    "expensive": {"min": 500000, "max": float('inf'), "label": "Trên 500k"}
}

# Số điện thoại khẩn cấp Việt Nam
EMERGENCY_CONTACTS = {
    "ambulance": {"number": "115", "name": "Cấp cứu", "available_247": True},
    "police": {"number": "113", "name": "Công an", "available_247": True},
    "fire": {"number": "114", "name": "Cứu hỏa", "available_247": True},
    "tourism_hotline": {"number": "1900 1188", "name": "Tổng đài du lịch Việt Nam", "available_247": True},
    "traffic_police": {"number": "0693", "name": "CSGT đường bộ", "available_247": False}
}

# Thông tin mùa du lịch
TRAVEL_SEASONS = {
    "north": {
        "spring": {"months": [1, 2, 3], "description": "Xuân - Thời tiết mát mẻ, phù hợp tham quan"},
        "summer": {"months": [4, 5, 6, 7, 8], "description": "Hè - Nóng ẩm, thích hợp nghỉ mát"},
        "autumn": {"months": [9, 10, 11], "description": "Thu - Khô ráo, thời tiết đẹp nhất"},
        "winter": {"months": [12], "description": "Đông - Lạnh, có thể có sương mù"}
    },
    "central": {
        "dry_season": {"months": [1, 2, 3, 4, 5, 6, 7, 8], "description": "Mùa khô - Thời tiết đẹp"},
        "rainy_season": {"months": [9, 10, 11, 12], "description": "Mùa mưa - Hay có bão"}
    },
    "south": {
        "dry_season": {"months": [11, 12, 1, 2, 3, 4], "description": "Mùa khô - Nắng đẹp"},
        "rainy_season": {"months": [5, 6, 7, 8, 9, 10], "description": "Mùa mưa - Mưa chiều"}
    }
}

# Loại dịch vụ đặt
SERVICE_TYPES = {
    "tour": "Tour du lịch",
    "hotel": "Khách sạn",
    "flight": "Vé máy bay",
    "train": "Vé tàu hỏa",
    "bus": "Vé xe khách",
    "attraction": "Vé tham quan",
    "restaurant": "Nhà hàng"
}

# Loại chỗ ở
ACCOMMODATION_TYPES = {
    "hotel": "Khách sạn",
    "resort": "Resort",
    "homestay": "Homestay",
    "hostel": "Hostel",
    "villa": "Villa",
    "apartment": "Căn hộ"
}

# Phương tiện di chuyển
TRANSPORTATION_TYPES = {
    "plane": "Máy bay",
    "train": "Tàu hỏa",
    "bus": "Xe khách",
    "car": "Xe ô tô",
    "motorbike": "Xe máy",
    "bicycle": "Xe đạp",
    "boat": "Tàu thuyền"
}

# Ngân sách du lịch (VNĐ/ngày/người)
BUDGET_RANGES = {
    "backpacker": {"min": 0, "max": 500000, "label": "Tiết kiệm (< 500k/ngày)"},
    "mid_range": {"min": 500000, "max": 1500000, "label": "Trung bình (500k - 1.5tr/ngày)"},
    "luxury": {"min": 1500000, "max": float('inf'), "label": "Cao cấp (> 1.5tr/ngày)"}
}

# Cảnh báo du lịch
WARNING_TYPES = {
    "weather": "Cảnh báo thời tiết",
    "natural_disaster": "Thiên tai",
    "epidemic": "Dịch bệnh",
    "traffic": "Giao thông",
    "security": "An ninh",
    "closed": "Đóng cửa tạm thời"
}

# Đánh giá chất lượng
RATING_CATEGORIES = {
    "destination": "Điểm đến",
    "tour": "Tour du lịch",
    "hotel": "Khách sạn",
    "restaurant": "Nhà hàng",
    "guide": "Hướng dẫn viên",
    "transportation": "Phương tiện",
    "chatbot": "Chatbot hỗ trợ"
}

# Các nền tảng tích hợp
PLATFORM_INTEGRATIONS = {
    "zalo": {"name": "Zalo", "qr_enabled": True},
    "messenger": {"name": "Facebook Messenger", "qr_enabled": True},
    "whatsapp": {"name": "WhatsApp", "qr_enabled": True},
    "instagram": {"name": "Instagram", "qr_enabled": False},
    "telegram": {"name": "Telegram", "qr_enabled": True},
    "viber": {"name": "Viber", "qr_enabled": True}
}

# Ngôn ngữ hỗ trợ
SUPPORTED_LANGUAGES = {
    "vi": "Tiếng Việt",
    "en": "English",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
    "fr": "Français",
    "es": "Español",
    "de": "Deutsch"
}