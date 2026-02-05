import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslationService } from './translation.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  translations$!: import('rxjs').Observable<Record<string,string>>;
  currentLang$!: import('rxjs').Observable<string>;
  lang = 'ru';
  langs = [
    { code: 'ru', label: 'Русский' },
    { code: 'en', label: 'English' }
  ];
  subjects = ['Mathematics', 'Physics', 'History'];
  topics = ['Algebra', 'Geometry', 'Mechanics', 'Optics', 'World War II'];
  selectedSubject = this.subjects[0];
  selectedTopics: string[] = [];
  actionClicked = false;

  constructor(private translationService: TranslationService) {
    this.translations$ = this.translationService.translations$;
    this.currentLang$ = this.translationService.currentLang$;
    this.translationService.setLang(this.lang);
    // set initial document title
    const t = this.translationService.instant('title');
    if (t) {
      document.title = t;
    }
    // subscribe to translations and update document title on language change
    this.translations$.subscribe(map => {
      if (map && map['title']) {
        document.title = map['title'];
      }
    });
  }

  setLang(code: string) {
    this.lang = code;
    this.translationService.setLang(code);
    const t = this.translationService.instant('title');
    if (t) {
      document.title = t;
    }
  }

  onSubjectChange(value: string) {
    this.selectedSubject = value;
  }

  onTopicsChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const selected: string[] = [];
    for (const option of Array.from(target.options)) {
      if (option.selected) {
        selected.push(option.value);
      }
    }
    this.selectedTopics = selected;
  }

  generateTasks() {
    this.actionClicked = true;
  }
}

