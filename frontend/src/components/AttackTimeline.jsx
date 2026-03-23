import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { getTimeline } from "../api/replay";

export default function AttackTimeline() {
  const [entityId, setEntityId] = useState("");
  const [entityType, setEntityType] = useState("session");

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["timeline", entityType, entityId],
    queryFn: () => getTimeline(entityType, entityId),
    enabled: false,
  });

  const handleLoad = () => {
    if (!entityId) return;
    refetch();
  };

  // ✅ FIXED POSITION
  const events = data?.timeline || [];

  return (
    <div className="bg-gray-900 p-4 rounded-xl shadow-md mt-6">
      <h2 className="text-xl font-semibold mb-4 text-white">
        Attack Timeline
      </h2>

      {/* Input */}
      <div className="flex gap-2 mb-4">
        <select
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
          className="bg-gray-800 text-white px-2 py-1 rounded"
        >
          <option value="session">Session</option>
          <option value="user">User</option>
          <option value="ip">IP</option>
          <option value="file">File</option>
        </select>

        <input
          type="text"
          placeholder="Entity ID"
          value={entityId}
          onChange={(e) => setEntityId(e.target.value)}
          className="flex-1 bg-gray-800 text-white px-3 py-1 rounded"
        />

        <button
          onClick={handleLoad}
          className="bg-purple-600 px-4 py-1 rounded"
        >
          Load
        </button>
      </div>

      {/* States */}
      {isLoading && <div className="text-gray-400">Loading...</div>}
      {error && <div className="text-red-500">Error loading timeline</div>}

      {/* Timeline */}
      {events.length === 0 && !isLoading && (
        <div className="text-gray-400">No events found</div>
      )}

      {events.length > 0 && (
        <div className="space-y-4 border-l-2 border-gray-700 pl-4">
          {events.map((event, index) => (
            <div key={index} className="relative">
              <div className="absolute -left-3 top-1 w-2 h-2 bg-blue-400 rounded-full"></div>

              <div className="bg-gray-800 p-3 rounded-lg">
                <div className="flex justify-between text-sm">
                  <span className="text-purple-400">
                    {event.module}
                  </span>
                  <span className="text-gray-400">
                    {new Date(event.time).toLocaleTimeString()}
                  </span>
                </div>

                <div className="text-white font-medium mt-1">
                  {event.signal}
                </div>

                <div
                  className={`text-xs mt-1 ${
                    event.severity === "high"
                      ? "text-red-400"
                      : event.severity === "medium"
                      ? "text-yellow-400"
                      : "text-green-400"
                  }`}
                >
                  Severity: {event.severity}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}