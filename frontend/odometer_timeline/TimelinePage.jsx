import React, { useEffect, useState } from 'react';
import { fetchOdometerTimeline } from './api';
import TimelineDay from './TimelineDay';
import TimelineLegend from './TimelineLegend';

export default function TimelinePage() {
  const [timeline, setTimeline] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [dateRange, setDateRange] = useState({ from: '', to: '' });

  useEffect(() => {
    fetchOdometerTimeline().then(setTimeline);
  }, []);

  // Filtering logic
  const filteredTimeline = timeline.filter(day => {
    // Range filter
    const dayDate = new Date(day.date);
    const fromDate = dateRange.from ? new Date(dateRange.from) : null;
    const toDate = dateRange.to ? new Date(dateRange.to) : null;
    const inRange = (!fromDate || dayDate >= fromDate) && (!toDate || dayDate <= toDate);

    // Search filter
    const searchMatch = day.events.some(event =>
      (event.location && event.location.toLowerCase().includes(searchQuery.toLowerCase())) ||
      (event.status && event.status.toLowerCase().includes(searchQuery.toLowerCase()))
    );

    return inRange && (searchQuery === '' || searchMatch);
  });

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Odometer Anomaly Timeline</h1>

      {/* Filters */}
      <div className="flex flex-wrap gap-4 mb-6 items-end">
        <div>
          <label className="block mb-1 font-medium">Search Location / Status</label>
          <input
            type="text"
            className="border px-3 py-2 rounded w-64"
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">From Date</label>
          <input
            type="date"
            className="border px-3 py-2 rounded"
            value={dateRange.from}
            onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
          />
        </div>
        <div>
          <label className="block mb-1 font-medium">To Date</label>
          <input
            type="date"
            className="border px-3 py-2 rounded"
            value={dateRange.to}
            onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
          />
        </div>
      </div>

      {/* Legend */}
      <TimelineLegend />

      {/* Timeline */}
      <div className="space-y-4">
        {filteredTimeline.length > 0 ? (
          filteredTimeline.map((day, idx) => (
            <TimelineDay key={idx} date={day.date} events={day.events} />
          ))
        ) : (
          <p>No matching results.</p>
        )}
      </div>
    </div>
  );
}
