import { useQuery } from "@tanstack/react-query";
import { getAnalytics } from "../../api/admin";

export default function AdminStats() {

  const { data, isLoading } = useQuery({

    queryKey: ["analytics"],

    queryFn: getAnalytics

  });

  if (isLoading) {

    return (
      <div className="text-gray-400">
        Loading analytics...
      </div>
    );

  }

  return (

    <div className="bg-gray-900 p-4 rounded-xl mt-6">

      <h2 className="text-xl text-white mb-4">
        System Analytics
      </h2>

      {/* MODULES */}

      <div className="mb-4">

        <h3 className="text-purple-400 mb-2">
          Module Usage
        </h3>

        {Object.entries(data.modules).map(
          ([key, val]) => (

            <div key={key}>

              {key}: {val}

            </div>

          )
        )}

      </div>

      {/* SEVERITY */}

      <div>

        <h3 className="text-yellow-400 mb-2">
          Severity Distribution
        </h3>

        {Object.entries(data.severity).map(
          ([key, val]) => (

            <div key={key}>

              {key}: {val}

            </div>

          )
        )}

      </div>

    </div>

  );
}