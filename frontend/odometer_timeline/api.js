export async function fetchOdometerTimeline() {
    const response = await fetch('/api/odometer-timeline');
    const data = await response.json();
    return data;
  }
  