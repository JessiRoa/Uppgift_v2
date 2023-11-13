CREATE TABLE public.results (
    id SERIAL,
    original INT,
    producer INT,
    saved TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    factors VARCHAR(1000)
);

CREATE TABLE public.preferences (
    preferences_key VARCHAR(10) NOT NULL,
    preferences_value INT DEFAULT 0
);

INSERT INTO public.preferences 
    (preferences_key, preferences_value)
VALUES
    ('enabled', 0)
;

-- INSERT INTO public.results 
--     (original, factors, saved)
-- VALUES
--     (2, '2', '2023-01-01'),
--     (3, '3', '2023-01-01')
-- ;
