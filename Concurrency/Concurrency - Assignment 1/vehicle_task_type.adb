-- @Author: Abu Abraham (u6325322)

with Ada.Real_Time;              use Ada.Real_Time;
with Exceptions;                 use Exceptions;
with Vehicle_Interface;          use Vehicle_Interface;
with Vehicle_Message_Type;       use Vehicle_Message_Type;
with Swarm_Structures;           use Swarm_Structures;
with Swarm_Structures_Base; use Swarm_Structures_Base;

package body Vehicle_Task_Type is

   -- Function to organize the vehicles areound the globe. Vehicles are arranged
   -- on 3 axis with distance from globe based on charge left. The lesser the
   -- charge, closer it gets.
   function updateCoordinates (vehicle_coordinates : Vector_3D; vehicle_number : Positive; vehicle_charge : Real) return Vector_3D is
      vehicle_coordinates_temp : Vector_3D := vehicle_coordinates;
   begin
      if vehicle_number mod 3 = 0 then
         vehicle_coordinates_temp (x) := vehicle_coordinates (x) -  vehicle_charge;
      elsif vehicle_number mod 3  = 1 then
        vehicle_coordinates_temp (y) := vehicle_coordinates (y) - vehicle_charge;
      else
         vehicle_coordinates_temp (z) := vehicle_coordinates (z) - vehicle_charge;
      end if;
      return vehicle_coordinates_temp;
   end updateCoordinates;

   task body Vehicle_Task is
      Updated : Boolean := False;
      Vehicle_No : Positive;

   begin

      accept Identify (Set_Vehicle_No : Positive; Local_Task_Id : out Task_Id) do
         Vehicle_No     := Set_Vehicle_No;
         Local_Task_Id  := Current_Task;
      end Identify;

      select
         Flight_Termination.Stop;

      then abort

         Outer_task_loop : loop

            Wait_For_Next_Physics_Update;

            declare
               Globes_Around : constant Energy_Globes := Energy_Globes_Around;
               Incoming_Message : Internal_Message;
               Local_Time : Time := Clock;
               Message_Local_Temp : Internal_Message;
               Vehicle_Message : Internal_Message;
               Count : Positive := 1;

               -- Function to find distance between 2 positions.
               function distanceBetween (position_1 : Vector_3D; position_2 : Vector_3D) return Real is
               begin
                  return ((position_1 (x) - position_2 (x))**2 + (position_1 (y) - position_2 (y))**2 + (position_1 (z) - position_2 (z))**2);
               end distanceBetween;

               -- Function to check whether the new potential target is closer to the vehicle than the old target.
               function closerGlobe (current_position : Vector_3D; current_target : Vector_3D; potential_target : Vector_3D) return Boolean is
               begin
                  if distanceBetween (current_position, current_target) > distanceBetween (current_position, potential_target) then
                     return False;
                  else
                     return True;
                  end if;
               end closerGlobe;

               -- Procedure to recursively find the latest message and update
               -- Vehicle_Message_Type.
               procedure findEneryGlobe is
               begin
                  -- If messages are waiting, iterate and find the latest one.
                  -- Else delay slightly and wait if charge is low or letroam.
                  if Messages_Waiting then
                     Updated := False;
                     Vehicle_Interface.Receive (Incoming_Message);
                     Message_Local_Temp := Incoming_Message;
                     Local_Time := Incoming_Message.Message_Time;
                     Vehicle_Message.Position := Incoming_Message.Position;
                     -- To check for the latest message
                     while Messages_Waiting loop
                        Vehicle_Interface.Receive (Incoming_Message);
                        if Local_Time < Incoming_Message.Message_Time then
                           Message_Local_Temp := Incoming_Message;
                           -- If a new message is found, and distance to the new
                           -- globe is less than earlier one and also, if there
                           -- is enough charge. Then go the new target.
                           if closerGlobe (Vehicle_Interface.Position, Vehicle_Message.Position, Incoming_Message.Position) and then Vehicle_Interface.Current_Charge > 0.1 then
                              Local_Time := Incoming_Message.Message_Time;
                                 Vehicle_Message.Position := Incoming_Message.Position;
                              if Incoming_Message.Vehicle_Presence (1) then
                                 Vehicle_Message_Type.Vehicle_Presence_Temp := Incoming_Message.Vehicle_Presence;
                              end if;
                              Updated := True;
                           end if;
                        end if;
                     end loop;
                     -- If no charge left (<0.1), move to the target mentioned in
                     -- last message.
                     if Updated = False then
                        Local_Time := Message_Local_Temp.Message_Time;
                        Vehicle_Message.Position := Message_Local_Temp.Position;
                     end if;
                  else
                     if Vehicle_Interface.Current_Charge < 0.5 then
                        delay 0.1;
                        findEneryGlobe;
                     else
                        Vehicle_Interface.Set_Throttle (0.0);
                     end if;

                  end if;

               end findEneryGlobe;


            begin
               -- If any globe is nearby, move to that globe in an organized way
               -- (Achieved through updateCoordinates() and setting the throtte
               -- based on charge left)
               -- Else if no globes are found nearby, recieve messages (Achieved
               -- through findEnergyGlobe) from other vehicles and set throtte
               -- based on charge left
               if Globes_Around'Length > 0 then
                  Incoming_Message.Position := Globes_Around (Globes_Around'First).Position;
                  Incoming_Message.Message_Time := Local_Time;
                  Vehicle_Message.Position := Incoming_Message.Position;
                  Vehicle_Message.Position := updateCoordinates (Vehicle_Message.Position, Vehicle_No, Long_Float (Vehicle_Interface.Current_Charge));
                  Vehicle_Interface.Set_Destination (Vehicle_Message.Position);
                  Vehicle_Interface.Set_Throttle (1.0 - Long_Float (Vehicle_Interface.Current_Charge));

               else
                  findEneryGlobe;
                  Incoming_Message.Position := Vehicle_Message.Position;
                  Incoming_Message.Message_Time := Local_Time;
                  Vehicle_Interface.Set_Destination (Incoming_Message.Position);
                  Vehicle_Interface.Set_Throttle (1.0 - Long_Float (Vehicle_Interface.Current_Charge));
               end if;

               -- Update the message to be sent with latest information.
               Incoming_Message.Vehicle_Presence := Vehicle_Message_Type.Vehicle_Presence_Temp;
               Incoming_Message.Vehicle_No := Vehicle_No;
               -- For part-d, mark presence of vehicle in boolean array.
               Incoming_Message.Vehicle_Presence (Vehicle_No) := True;

               -- For part-d, iterate through the boolean array, representing
               -- presence of vehicles and count the number of active ones.
               for I in Incoming_Message.Vehicle_Presence'Range loop
                  if Incoming_Message.Vehicle_Presence (I) then
                     Count := Count + 1;
                  end if;
               end loop;
               -- If more than the threshold is found, kill the current vehicle
               -- by letting it roam freely.
               if Count > (Vehicle_Interface.Target_No_of_Elements+1) and then Incoming_Message.Vehicle_Presence (Vehicle_No) then
                  Incoming_Message.Vehicle_Presence (Vehicle_No) := False;
                  Flight_Termination.Stop;
               end if;

               -- Send the updated message
               Vehicle_Interface.Send (Message => Incoming_Message);
            end;

         end loop Outer_task_loop;

      end select;

   exception
      when E : others => Show_Exception (E);

   end Vehicle_Task;

end Vehicle_Task_Type;
