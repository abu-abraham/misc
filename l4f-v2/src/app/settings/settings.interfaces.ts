import { LingusiticValues } from "../config.service";

export interface iSettings {
    no_of_solutions: number;
    time_limit: number;
    preset_limit: number;
    print_finder_job: LingusiticValues;
    print_solutions: LingusiticValues;
    print_statistics: LingusiticValues;
}
