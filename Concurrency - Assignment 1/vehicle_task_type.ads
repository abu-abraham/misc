with Ada.Task_Identification; use Ada.Task_Identification;
with Vectors_3D;            use Vectors_3D;
with Real_Type; use Real_Type;


package Vehicle_Task_Type is

   function updateCoordinates (vehicle_coordinates :  Vector_3D; vehicle_number : Positive; vehicle_charge  : Real) return Vector_3D;

   task type Vehicle_Task is
      entry Identify (Set_Vehicle_No : Positive; Local_Task_Id : out Task_Id);
   end Vehicle_Task;


end Vehicle_Task_Type;
