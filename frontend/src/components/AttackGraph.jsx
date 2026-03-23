import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import { getGraph } from "../api/graph";

export default function AttackGraph() {
  const svgRef = useRef();
  const [entityId, setEntityId] = useState("");
  const [entityType, setEntityType] = useState("session");
  const [data, setData] = useState(null);

  const loadGraph = async () => {
    if (!entityId) return;

    try {
        const res = await getGraph(entityType, entityId);

        console.log("GRAPH API RESPONSE:", res);

        setData(res.graph);   // 🔥 FIX HERE

    } catch (err) {
        console.error("GRAPH ERROR:", err);
    }
    };

  useEffect(() => {
    if (!data || !data.nodes || !data.links) {
    console.log("INVALID GRAPH DATA:", data);
    return;
    }
    console.log("GRAPH DATA:", data);
    console.log("LINK DATA:", data.links);
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const width = 500;
    const height = 400;

    const simulation = d3
      .forceSimulation([...data.nodes])
      .force(
        "link",
        d3.forceLink(data.links).id((d) => d.id).distance(120).strength(0.8)
      )
      .force("charge", d3.forceManyBody().strength(-120))
      .force("collision",
        d3.forceCollide().radius(40)
      )
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append("g")
      .selectAll("line")
      .data(data.links)
      .enter()
      .append("line")
      .attr("stroke", "#888")
      .attr("stroke-width", d =>
          Math.sqrt(d.weight || 1)
      );

    const node = svg
      .append("g")
      .selectAll("circle")
      .data(data.nodes)
      .enter()
      .append("circle")
      .attr("r", d => {
        if (d.type === "module") return 8 + (d.count || 1);
        if (d.type === "signal") return 6 + (d.count || 1);
        return 10;
        })
      .attr("fill", (d) => {
        if (d.type === "entity") return "#22c55e";
        if (d.type === "module") return "#a855f7";
        if (d.type === "signal") {
            if (d.severity === "high")
            return "#ef4444";
            if (d.severity === "medium")
            return "#facc15";
            return "#3b82f6";
        }
        })
      .call(
        d3
          .drag()
          .on("start", dragStart)
          .on("drag", dragging)
          .on("end", dragEnd)
      );

    const label = svg
      .append("g")
      .selectAll("text")
      .data(data.nodes)
      .enter()
      .append("text")
      .text((d) => d.label || d.id)
      .attr("font-size", 10)
      .attr("fill", "white");

    simulation.on("tick", () => {
      link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

      node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

      label
        .attr("x", (d) => d.x + 10)
        .attr("y", (d) => d.y + 5);
    });

    function dragStart(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragging(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragEnd(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  }, [data]);

  return (
    <div className="bg-gray-900 p-4 rounded-xl mt-6">
      <h2 className="text-xl text-white mb-4">
        Attack Graph
      </h2>

      {/* Controls */}
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
          placeholder="Entity ID"
          value={entityId}
          onChange={(e) => setEntityId(e.target.value)}
          className="bg-gray-800 text-white px-3 py-1 rounded flex-1"
        />

        <button
          onClick={loadGraph}
          className="bg-green-600 px-4 py-1 rounded"
        >
          Generate
        </button>
      </div>

      {/* Graph */}
      <svg ref={svgRef} width="500" height="400" />
    </div>
  );
}