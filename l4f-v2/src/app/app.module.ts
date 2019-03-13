import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {V2MaterialModule} from './material';
import { LoginComponent } from './login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { appRoutes } from './routes';

import { HttpService } from './shared/http.service';
import { AuthService } from './auth/auth.service';
import { HomeComponent } from './home/home.component';
import { SolverComponent } from './solver/solver.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ContenteditableModule } from 'ng-contenteditable';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { SolverPageComponent } from './solver-page/solver-page.component';
import { SettingsComponent } from './settings/settings.component';
import { FooterComponent } from './footer/footer.component';
import { FeedbackComponent } from './feedback/feedback.component';
import { FeedbackPageComponent } from './feedback-page/feedback-page.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    SolverComponent,
    ToolbarComponent,
    SolverPageComponent,
    SettingsComponent,
    FooterComponent,
    FeedbackComponent,
    FeedbackPageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    V2MaterialModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(appRoutes),
    ReactiveFormsModule,
    ContenteditableModule,
  ],
  providers: [HttpService, AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
