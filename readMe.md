# EndGame

### 개발목적

<hr>

1. 학습
2. 영화정보 제공

<br> 

### 사용기술

<hr>

Language : Python 3.6.7

OS : Linux (C9환경)

Database : SQLite3

Server :

Web : HTML, CSS

Framework : Django 2.1.8

ETC : Bootstrap

<br>

### 사용 라이브러리

```bash
# pyenv install
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc

echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc

exec "$SHELL"

# python version upgrade
pyenv install 3.6.7
pyenv global 3.6.7
pyenv rehash

# pip upgrade
pip install --upgrade pip

# install django
pip install django==2.1.8

#bootstrap
pip install django-bootstrap4
#ImageField & Resize_Image
pip install Pillow
pip install pilkit
pip install django-imagekit
```

```python
#modles.py
"""
사용법 참조 공식github
https://github.com/matthewwithanm/django-imagekit
"""
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
```

<br>

### 역할

<hr>

**문영국**
-MOVIE CRUD
-COMMENT CRUD

**조호근**
-account(자체 회원가입, Gravatar)

**정태준**
-all-auth(Google, Naver, Facebook)
-데이터 크롤링(영진사)

**[추가사항]**
@내 위치에서 가까운 영화관 추천
@다국어
@Slack/Telegram 알림