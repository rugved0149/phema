import { useQuery } from "@tanstack/react-query";
import { getSystemStatus } from "../../api/system";

export default function SystemStatus() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["systemStatus"],
    queryFn: getSystemStatus,
  });

  if (isLoading) {
    return <div className="text-gray-400">Loading system status...</div>;
  }

  if (error) {
    return (
      <div className="text-red-500">
        Failed to connect to backend
      </div>
    );
  }

  return (
    <div className="bg-gray-900 p-4 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-3 text-white">
        System Status
      </h2>

      <div className="mb-2">
        <span className="text-gray-400">Status: </span>
        <span className="text-green-400 font-bold">
          {data.status}
        </span>
      </div>

      <div>
        <span className="text-gray-400">Modules:</span>
        <ul className="mt-2 space-y-1">
          {data.modules.map((mod, index) => (
            <li
              key={index}
              className="bg-gray-800 px-3 py-1 rounded text-sm text-gray-200"
            >
              {mod}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}