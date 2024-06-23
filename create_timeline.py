import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Initialize style parameters
plt.rcParams['figure.dpi'] = 1000
plt.style.use('science')

# Function to create a timeline
def create_timeline(start_date, end_date, gaps):
    # Convert dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Create date range excluding gaps
    current_date = start_date
    dates = []
    
    while current_date <= end_date:
        if not any(start <= current_date <= end for start, end in gaps):
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Prepare the dates for major ticks
    major_ticks = [start_date] + [date for gap in gaps for date in gap] + [end_date]
    
    # Plotting the timeline
    fig, ax = plt.subplots(figsize=(15, 3))
    
    ax.plot(dates, [1] * len(dates), marker='o', linestyle='None', color='#4358cb')
    
    # Formatting the plot
    ax.set_xticks(major_ticks)
    ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in major_ticks], fontsize=22)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.yaxis.set_visible(False)
    plt.xlabel('Date', fontsize=24)
    
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Define the start and end dates
start_date = '1972-12-17'
end_date = '1973-10-31'

# Define gaps as tuples of (start_date, end_date)
gaps = [
    (datetime(1973, 3, 6), datetime(1973, 4, 15)),
    (datetime(1973, 4, 30), datetime(1973, 6, 17)),
    (datetime(1973, 6, 30), datetime(1973, 8, 11)),
    (datetime(1973, 8, 31), datetime(1973, 10, 14)),
]

# Create the timeline
create_timeline(start_date, end_date, gaps)
