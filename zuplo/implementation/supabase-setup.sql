-- Create events table
CREATE TABLE events (
  id SERIAL PRIMARY KEY,
  time TIMESTAMP NOT NULL,
  event_id TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- Create policy that allows reading all rows
CREATE POLICY "Allow read access for all users" ON events
  FOR SELECT USING (true);

-- Insert sample data
INSERT INTO events (time, event_id)
VALUES
  ('2025-01-01 10:00:00', '123'),
  ('2025-01-01 11:00:00', '124'),
  ('2025-01-01 12:00:00', '125'),
  ('2025-01-02 10:00:00', '126'),
  ('2025-01-02 11:00:00', '127');
