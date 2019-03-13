import { Component, OnInit } from '@angular/core';
import { iSettings } from './settings.interfaces';
import { ConfigService , LingusiticValues} from '../config.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})



export class SettingsComponent implements OnInit {
  public selected_no_of_solutions: number;
  public selected_time_limit: number;
  public selected_pretest_limit: number;
  public selected_print_finder_job: LingusiticValues;
  public selected_print_solutions: LingusiticValues;;
  public selected_print_statistics: LingusiticValues;

  private initial_settings: iSettings;

  public options_4_no_of_solutions: number[] = [1, 2, 3, 4, 5];
  public options_4_time_limit: number[] = [1, 2, 3, 4, 5];
  public options_4_pretest_limit: number[] = [1, 2, 3, 4, 5];
  public options_4_print_finder_job: LingusiticValues[] = [LingusiticValues.None, LingusiticValues.Brief, LingusiticValues.Full];
  public options_4_print_solutions: LingusiticValues[] = [LingusiticValues.None, LingusiticValues.Brief, LingusiticValues.Full];
  public options_4_print_statistics: LingusiticValues[] = [LingusiticValues.None, LingusiticValues.Brief, LingusiticValues.Full];

  constructor(public config: ConfigService) {
    this.initial_settings = this.config.getSettings();
    this.selected_no_of_solutions = this.initial_settings.no_of_solutions;
    this.selected_time_limit = this.initial_settings.time_limit;
    this.selected_pretest_limit = this.initial_settings.preset_limit;
    this.selected_print_finder_job = this.initial_settings.print_finder_job;
    this.selected_print_solutions = this.initial_settings.print_solutions;
    this.selected_print_statistics = this.initial_settings.print_statistics;
  }

  ngOnInit() {
  }

  public onSave(): void {
    this.initial_settings.no_of_solutions = this.selected_no_of_solutions;
    this.initial_settings.time_limit = this.selected_time_limit;
    this.initial_settings.preset_limit = this.selected_pretest_limit;
    this.initial_settings.print_finder_job = this.selected_print_finder_job;
    this.initial_settings.print_solutions = this.selected_print_solutions;
    this.initial_settings.print_statistics = this.selected_print_statistics;
    this.config.setSettings(this.initial_settings);
  }
}