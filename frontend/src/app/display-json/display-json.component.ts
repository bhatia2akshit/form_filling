import { Component, OnInit } from '@angular/core';
import { MatListModule } from '@angular/material/list';
import { DocumentService } from '../services/document.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-display-json',
  standalone: true,
  imports: [MatListModule, CommonModule],
  templateUrl: './display-json.component.html',
  styleUrl: './display-json.component.scss'
})
export class DisplayJsonComponent implements OnInit {
  jsonData: any = null;
  isLoading: boolean = false;
  error: string | null = null;

  constructor(
    private documentService: DocumentService
  ) {}

  ngOnInit() {
    this.loadCombinedJson();
  }

  loadCombinedJson() {
    this.isLoading = true;
    this.error = null;
    this.documentService.getCombinedJson().subscribe({
      next: (data) => {
        this.jsonData = data;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = 'Failed to load JSON data';
        this.isLoading = false;
      }
    });
  }
}
