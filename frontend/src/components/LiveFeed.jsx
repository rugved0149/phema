import { useQuery } from "@tanstack/react-query";
import { getLiveEvents } from "../api/correlation";

export default function LiveFeed() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["liveEvents"],
    queryFn: getLiveEvents,
    refetchInterval: 3000,
  });

  if (isLoading) {
    return <div className="text-gray-400">Loading events...</div>;
  }

  if (error) {
    return <div className="text-red-500">Failed to load events</div>;
  }

  // 🔥 CRITICAL FIX
  const events = Array.isArray(data) ? data : data?.events || [];

  return (
    <div className="bg-gray-900 p-4 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-3 text-white">
        Live Threat Feed
      </h2>

      {events.length === 0 ? (
        <div className="text-gray-400 text-sm">
          No recent activity
        </div>
      ) : (
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {events.map((event, index) => (
            <div
              key={index}
              className="bg-gray-800 p-3 rounded-lg border border-gray-700"
            >
              <div className="flex justify-between text-sm">
                <span className="text-purple-400">
                  {event.module}
                </span>
                <span className="text-gray-400">
                  {event.timestamp}
                </span>
              </div>

              <div className="text-white font-medium mt-1">
                {event.signal}
              </div>

              <div className="text-xs text-gray-400 mt-1">
                Entity: {event.entity_id}
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
          ))}
        </div>
      )}
    </div>
  );
}