import React, { useState } from 'react';

export default function TimelineDay({ date, events }) {
  const [selectedEvent, setSelectedEvent] = useState(null);

  return (
    <div className="flex flex-col mb-4">
      <div className="flex items-center">
        <div className="w-24 font-bold">{date}</div>
        <div className="flex gap-2">
          {events.map((event, idx) => (
            <div key={idx}>
              <div
                onClick={() => setSelectedEvent(event)}
                className="w-4 h-4 rounded-full cursor-pointer transition-transform transform hover:scale-125"
                style={{
                  backgroundColor:
                    event.status === "normal"
                      ? "green"
                      : event.status === "anomaly_drop"
                      ? "red"
                      : "yellow"
                }}
                title={`${event.time} - ${event.status}`}
              ></div>
            </div>
          ))}
        </div>
      </div>

      {/* Modal */}
      {selectedEvent && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-80">
            <h2 className="text-xl font-bold mb-4">Event Details</h2>
            <p><strong>Date:</strong> {date}</p>
            <p><strong>Time:</strong> {selectedEvent.time}</p>
            <p><strong>Status:</strong> {selectedEvent.status}</p>
            <p className="text-gray-600"></p><p><strong>Location:</strong> {selectedEvent.location || "Unknown"}</p>
            <p><strong>Odometer:</strong> {selectedEvent.odometer || "N/A"} miles</p>
            <button
              className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              onClick={() => setSelectedEvent(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
