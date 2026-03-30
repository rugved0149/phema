export default function RiskBadge({ level }){

  const getStyle=()=>{

    switch(level){

      case "HIGH":
        return "bg-red-500 text-white";

      case "MEDIUM":
        return "bg-yellow-400 text-black";

      case "LOW":
        return "bg-green-500 text-white";

      default:
        return "bg-gray-400 text-white";

    }

  };

  return(

    <span
      className={`px-2 py-1 rounded text-xs font-semibold ${getStyle()}`}
      style={{ display:"inline-block" }}
    >
      {level}
    </span>

  );

}