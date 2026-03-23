import SystemStatus from "./components/SystemStatus";
import LiveFeed from "./components/LiveFeed";
import EntityInvestigation from "./components/EntityInvestigation";
import AttackTimeline from "./components/AttackTimeline";
import AttackGraph from "./components/AttackGraph";

export default function App() {
  return (
    <div className="min-h-screen bg-black text-white p-6">
      <h1 className="text-3xl font-bold mb-6">
        PHEMA Security Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SystemStatus />
        <LiveFeed />
      </div>

      <div className="mt-6">
        <EntityInvestigation />
      </div>

      <div className="mt-6">
        <AttackTimeline />
      </div>

      <div className="mt-6">
        <AttackGraph />
      </div>

    </div>
  );
}