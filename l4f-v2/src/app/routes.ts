import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { SolverComponent } from './solver/solver.component';
import { SolverPageComponent } from './solver-page/solver-page.component';
import { SettingsComponent } from './settings/settings.component';
import { FeedbackPageComponent } from './feedback-page/feedback-page.component';


export const appRoutes : Routes = [
    { path: 'login', component: LoginComponent},
    { path: 'home', component: HomeComponent},
    { path: 'solver', component: SolverPageComponent},
    { path: 'settings', component: SettingsComponent},
    { path: 'feedback', component: FeedbackPageComponent},
    { path: '', redirectTo: '/login', pathMatch: 'full'}
];