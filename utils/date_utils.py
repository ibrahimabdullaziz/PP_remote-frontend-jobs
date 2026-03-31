from datetime import datetime, timezone
import re

def get_age_hours(time_str: str) -> float:
    """
    Convert various time strings into age in hours.
    Supported:
    - LinkedIn relative: '2 hours ago', '1 day ago', 'Recently'
    - ISO dates: '2024-03-31T10:00:00Z'
    - Short dates: '2024-03-31'
    """
    now = datetime.now(timezone.utc)
    time_str = time_str.lower().strip()

    # 1. Relative Time (LinkedIn)
    if 'ago' in time_str or 'recently' in time_str:
        if 'recently' in time_str or 'just' in time_str:
            return 0.5
        
        match = re.search(r'(\d+)\s+(minute|hour|day|week|month)', time_str)
        if not match:
            return 24.0 # Default to 1 day if unknown
            
        val = int(match.group(1))
        unit = match.group(2)
        
        if 'minute' in unit: return val / 60
        if 'hour' in unit: return val
        if 'day' in unit: return val * 24
        if 'week' in unit: return val * 24 * 7
        if 'month' in unit: return val * 24 * 30
    
    # 2. ISO / Date strings
    try:
        # Try full ISO
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = now - dt
        return max(0, delta.total_seconds() / 3600)
    except:
        pass

    try:
        # Try YYYY-MM-DD
        dt = datetime.strptime(time_str[:10], '%Y-%m-%d').replace(tzinfo=timezone.utc)
        delta = now - dt
        return max(0, delta.total_seconds() / 3600)
    except:
        pass

    return 0.0 # Default to brand new if totally unknown
