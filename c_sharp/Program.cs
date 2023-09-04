using System;
using System.Threading;
using WootingAnalogSDKNET;
using Serilog;
using System.IO;

namespace c_sharp
{

    class Program
    {
        
        static void callback(DeviceEventType eventType, DeviceInfo deviceInfo) {
            Console.WriteLine($"Device event cb called with: {eventType} {deviceInfo}");
        }


        static void Main(string[] args){
            // create file to init columns
            using (StreamWriter sw = File.CreateText($"logging/{args[0]}_{args[1]}_{args[2]}analog_logging.log")){
                sw.Write("time|perif|location|event\n");
            }
            string timeFormat = "yyyy-MM-dd HH:mm:ss.fffff";//"HH:mm:ss.fffff";
            Console.WriteLine(args[0]);
            Log.Logger = new LoggerConfiguration()
                .MinimumLevel.Debug()
                .WriteTo.Console()
                .WriteTo.File($"logging/{args[0]}_{args[1]}_{args[2]}analog_logging.log", outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fffff}{Message:l}{NewLine}")//, rollingInterval: RollingInterval.Day, outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fffff}|{Message:l}{NewLine}")
                .CreateLogger();

            Log.Information($"|analog|gen|init");

            // https://github.com/WootingKb/wooting-analog-wrappers/blob/master/examples/GUIDE.md
            var (noDevices, error) = WootingAnalogSDK.Initialise(); 
            // If the number of devices is at least 0 it indicates the initialisation was successful
            if (noDevices >= 0) {
                Console.WriteLine($"{DateTime.Now.ToString(timeFormat)}: Analog SDK Successfully initialised with {noDevices} devices!");
				
                // Subscribe to the DeviceEvent
                WootingAnalogSDK.DeviceEvent += callback;


                // Get a list of the connected devices and Associated information
                var (devices, infoErr) = WootingAnalogSDK.GetConnectedDevicesInfo();
                if (infoErr != WootingAnalogResult.Ok)
                    Console.WriteLine($"Error getting devices: {infoErr}");

                foreach (DeviceInfo device in devices)
                {
                    Console.WriteLine($"{DateTime.Now.ToString(timeFormat)}: Device info has: {device}");
                }

                // This can be used to make the SDK give you keycodes from the Windows Virtual Key set that are translated based on the language set in Windows
                // By default the keycodes the SDK will give you are the HID keycodes
                //WootingAnalogSDK.SetKeycodeMode(KeycodeType.VirtualKeyTranslate);
				
                while (true) {
                    var (keys, readErr) = WootingAnalogSDK.ReadFullBuffer(20);
                    if (readErr == WootingAnalogResult.Ok)
                    {
                        // Go through all the keys that were read and output them
                        foreach (var analog in keys)
                        {
                            Console.Write($"{DateTime.Now.ToString(timeFormat)}: ({analog.Item1},{analog.Item2})");
                            Log.Information($"|analog|{analog.Item1}|{analog.Item2}");
                        }
		
                        // We want to put on the new line character only if keys have been read and output to the console
                        if (keys.Count > 0)
                            Console.WriteLine();
                    }
                    else
                    {
                        Console.WriteLine($"{DateTime.Now.ToString(timeFormat)}Read failed with {readErr}");
                        // We want to put more of a delay in when we get an error as we don't want to spam the log with the errors
			            Thread.Sleep(1000);
                    }

                    // We want to have a bit of a delay so we don't spam the console with new values
                    //Thread.Sleep(100);
                    //Log.Debug($"{DateTime.Now.ToString(timeFormat)}|analog|gen|done");
                }
            }			
            else {
                Console.WriteLine($"Analog SDK failed to initialise: {error}");
            }
        }
    }
}
