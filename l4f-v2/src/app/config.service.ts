import { Injectable } from '@angular/core';
import { iSettings } from './settings/settings.interfaces';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  public ms_access_token: string;
  public google_access_token: string;

  constructor() { }

  public getSettings(): iSettings {
    const stored_setting = sessionStorage.getItem("l4f_settings");
    let settings: iSettings;
    if (stored_setting != undefined && stored_setting != null) {
      settings = JSON.parse(stored_setting);
    }
    else {
      settings = <iSettings>{
        no_of_solutions: 3,
        time_limit: 3,
        preset_limit: 3,
        print_finder_job: LingusiticValues.None,
        print_solutions: LingusiticValues.Full,
        print_statistics: LingusiticValues.Brief
      }
    }
    return settings;
  }

  public setSettings(settings: iSettings): void {
    sessionStorage.setItem("l4f_settings", JSON.stringify(settings));
  }
}


export enum LingusiticValues {
  None = "None",
  Brief = "Brief",
  Full = "Full"
};
