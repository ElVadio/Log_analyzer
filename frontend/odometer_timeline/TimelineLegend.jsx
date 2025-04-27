import React from 'react';

export default function TimelineLegend() {
  const items = [
    { color: 'green', label: 'Normal Movement' },
    { color: 'red', label: 'Odometer Drop' },
    { color: 'yellow', label: 'Data Missing' },
  ];

  return (
    <div className="flex gap-8 mb-8 items-center">
      {items.map((item, idx) => (
        <div key={idx} className="flex items-center gap-2">
          <div
            className="w-4 h-4 rounded-full"
            style={{ backgroundColor: item.color }}
          ></div>
          <span className="text-sm">{item.label}</span>
        </div>
      ))}
    </div>
  );
}
