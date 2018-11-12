-- Suggestions for packages which might be useful:

with Ada.Real_Time;         use Ada.Real_Time;
with Vectors_3D;            use Vectors_3D;
with Swarm_Configuration; use Swarm_Configuration;

package Vehicle_Message_Type is

   -- Replace this record definition by what your vehicles need to communicate.

   type Boolean_Array is array (Positive range 1 .. Swarm_Configuration.Initial_No_of_Elements+20) of Boolean;

   Vehicle_Presence_Temp : Boolean_Array;

   type Inter_Vehicle_Messages is record
      Position : Vector_3D;
      Message_Time : Time;
      Vehicle_No : Positive;
      Vehicle_Presence : Boolean_Array;
   end record;

   subtype Internal_Message is Inter_Vehicle_Messages;

end Vehicle_Message_Type;
