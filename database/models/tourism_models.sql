# app/database/models/tourism_models.sql

-- Bảng điểm đến du lịch
CREATE TABLE destinations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,  -- Tỉnh/thành phố
    attraction_type VARCHAR(100),  -- Loại điểm tham quan
    description TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    opening_hours VARCHAR(255),
    price_info TEXT,  -- JSON: {adult: 100000, child: 50000, ...}
    rating DECIMAL(3, 2),
    contact_info TEXT,  -- JSON: {phone, email, website}
    image_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_location (location),
    INDEX idx_type (attraction_type)
);

-- Bảng sự kiện/lễ hội
CREATE TABLE events_festivals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    event_type VARCHAR(50),  -- festival, cultural_event, sport_event
    description TEXT,
    start_date DATE,
    end_date DATE,
    month INT,  -- Tháng diễn ra (1-12)
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_location (location),
    INDEX idx_month (month)
);

-- Bảng tour du lịch
CREATE TABLE tours (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    destination VARCHAR(255),
    duration_days INT,
    price DECIMAL(15, 2),
    description TEXT,
    itinerary TEXT,  -- JSON: [{day: 1, activities: [...]}]
    includes TEXT,  -- JSON: [accommodation, meals, transport, ...]
    excludes TEXT,
    max_participants INT,
    tour_type VARCHAR(50),  -- group, private, adventure, culture
    image_url VARCHAR(500),
    rating DECIMAL(3, 2),
    status VARCHAR(20) DEFAULT 'active',  -- active, inactive
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Bảng đặt dịch vụ
CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id VARCHAR(100) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    service_type VARCHAR(50) NOT NULL,  -- tour, hotel, flight, attraction
    service_id INT,
    check_in DATE,
    check_out DATE,
    number_of_people INT,
    total_price DECIMAL(15, 2),

    -- Customer info
    customer_name VARCHAR(255),
    customer_phone VARCHAR(20),
    customer_email VARCHAR(255),

    -- Additional
    special_requests TEXT,
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending',  -- pending, paid, cancelled
    booking_status VARCHAR(20) DEFAULT 'confirmed',  -- confirmed, cancelled, completed

    confirmation_link VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_booking_id (booking_id)
);

-- Bảng đánh giá
CREATE TABLE reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    service_type VARCHAR(50),  -- destination, tour, hotel
    service_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    images TEXT,  -- JSON: [url1, url2, ...]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id),
    INDEX idx_service (service_type, service_id)
);

-- Bảng thông tin khẩn cấp
CREATE TABLE emergency_contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    location VARCHAR(255) NOT NULL,
    contact_type VARCHAR(50),  -- hospital, police, fire, tourism_support
    name VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(500),
    available_247 BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_location (location)
);

-- Bảng lịch trình được tạo
CREATE TABLE itineraries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    destination VARCHAR(255),
    duration_days INT,
    start_date DATE,
    budget DECIMAL(15, 2),
    preferences TEXT,  -- JSON: [preference1, preference2, ...]
    itinerary_data TEXT,  -- JSON: Chi tiết lịch trình
    status VARCHAR(20) DEFAULT 'draft',  -- draft, confirmed, completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_customer (customer_id)
);