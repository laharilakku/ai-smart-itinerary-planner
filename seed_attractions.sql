-- Sample Indian tourist attractions for testing

INSERT INTO users (name, email, hashed_password, preferred_currency) VALUES
    ('Lahari Lakku', 'lahari@smartitinerary.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'INR');

INSERT INTO attractions (name, category, latitude, longitude, city, country, rating, visit_duration_hrs, entry_fee, description, tags) VALUES
    -- Delhi
    ('Red Fort', 'heritage', 28.6562, 77.2410, 'Delhi', 'India', 4.5, 2.0, 35.0, 'Historic Mughal fort complex in Old Delhi.', '["heritage","history","mughal"]'),
    ('Qutub Minar', 'heritage', 28.5244, 72.2736, 'Delhi', 'India', 4.6, 1.5, 40.0, 'UNESCO World Heritage Site, tallest minaret in India.', '["heritage","UNESCO","history"]'),
    ('India Gate', 'monument', 28.6129, 77.2295, 'Delhi', 'India', 4.4, 1.0, 0.0, 'War memorial and iconic landmark.', '["monument","viewpoint","park"]'),
    ('Humayuns Tomb', 'heritage', 28.5933, 77.2508, 'Delhi', 'India', 4.5, 1.5, 35.0, 'Magnificent Mughal garden tomb.', '["heritage","UNESCO","garden"]'),
    ('Lotus Temple', 'temple', 28.5535, 77.2588, 'Delhi', 'India', 4.4, 1.0, 0.0, 'Stunning Bahai House of Worship.', '["temple","architecture","peaceful"]'),

    -- Agra
    ('Taj Mahal', 'heritage', 27.1751, 78.0421, 'Agra', 'India', 4.9, 3.0, 50.0, 'One of the Seven Wonders of the World.', '["heritage","UNESCO","romantic","wonder"]'),
    ('Agra Fort', 'heritage', 27.1795, 78.0211, 'Agra', 'India', 4.4, 2.0, 40.0, 'Massive Mughal fort along the Yamuna.', '["heritage","fort","mughal"]'),
    ('Fatehpur Sikri', 'heritage', 27.0945, 77.6679, 'Agra', 'India', 4.3, 2.5, 40.0, 'Deserted Mughal capital city.', '["heritage","UNESCO","history"]'),

    -- Jaipur
    ('Hawa Mahal', 'heritage', 26.9239, 75.8267, 'Jaipur', 'India', 4.5, 1.0, 50.0, 'Palace of Winds — iconic pink sandstone facade.', '["heritage","architecture","photography"]'),
    ('Amber Fort', 'fort', 26.9855, 75.8513, 'Jaipur', 'India', 4.7, 3.0, 100.0, 'Majestic hilltop fort with stunning views.', '["fort","heritage","viewpoint","adventure"]'),
    ('City Palace Jaipur', 'heritage', 26.9258, 75.8237, 'Jaipur', 'India', 4.4, 2.0, 200.0, 'Royal palace complex in the heart of the Pink City.', '["heritage","palace","museum"]'),
    ('Jantar Mantar', 'heritage', 26.9246, 75.8244, 'Jaipur', 'India', 4.2, 1.0, 50.0, 'UNESCO-listed astronomical observatory.', '["heritage","UNESCO","science"]'),

    -- Mumbai
    ('Gateway of India', 'monument', 18.9220, 72.8347, 'Mumbai', 'India', 4.4, 1.0, 0.0, 'Iconic arch monument on the Mumbai waterfront.', '["monument","waterfront","photography"]'),
    ('Elephanta Caves', 'heritage', 18.9633, 72.9315, 'Mumbai', 'India', 4.3, 3.0, 40.0, 'Rock-cut cave temples on Elephanta Island.', '["heritage","UNESCO","cave","island"]'),
    ('Marine Drive', 'viewpoint', 18.9438, 72.8231, 'Mumbai', 'India', 4.5, 1.5, 0.0, 'The Queens Necklace — scenic coastal boulevard.', '["viewpoint","waterfront","sunset","walk"]'),

    -- Hyderabad
    ('Charminar', 'heritage', 17.3616, 78.4747, 'Hyderabad', 'India', 4.4, 1.5, 25.0, 'Iconic 16th-century monument and mosque.', '["heritage","monument","architecture"]'),
    ('Golconda Fort', 'fort', 17.3833, 78.4011, 'Hyderabad', 'India', 4.5, 3.0, 15.0, 'Historic fort with brilliant acoustics and light shows.', '["fort","heritage","history","adventure"]'),
    ('Ramoji Film City', 'entertainment', 17.2543, 78.6808, 'Hyderabad', 'India', 4.3, 6.0, 1150.0, 'Worlds largest film studio complex.', '["entertainment","family-friendly","adventure"]');

-- Sample trip
INSERT INTO trips (user_id, title, destination, start_date, end_date, total_budget, currency, status) VALUES
    (1, 'Golden Triangle Tour', 'Delhi-Agra-Jaipur', '2026-12-20 00:00:00+00', '2026-12-26 00:00:00+00', 25000.0, 'INR', 'planned');
