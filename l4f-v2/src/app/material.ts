import {MatButtonModule, MatCheckboxModule} from '@angular/material';
import { NgModule } from '@angular/core';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon';
import {MatCardModule} from '@angular/material/card'
import {MatExpansionModule} from '@angular/material/expansion';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatButtonToggleModule} from '@angular/material/button-toggle';
import {MatMenuModule} from '@angular/material/menu';
import {MatSelectModule} from '@angular/material/select';
import { MatInputModule } from '@angular/material';
//All the matrila we nedd
@NgModule({
    imports: [MatButtonModule, MatCardModule, MatToolbarModule, MatIconModule, MatExpansionModule, MatFormFieldModule, MatInputModule, MatButtonToggleModule,MatMenuModule,MatSelectModule],
    exports: [MatButtonModule, MatCardModule, MatToolbarModule, MatIconModule, MatExpansionModule, MatFormFieldModule, MatInputModule, MatButtonToggleModule,MatMenuModule,MatSelectModule]
})

export class V2MaterialModule {}