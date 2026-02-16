---
title: "Настройка XKeen с помощью Windows"
slug: "configuring-xkeen-windows"
lang: "ru"
excerpt: "Полная и подробная инструкция по настройке XKeen на роутерах Keenetic в Windows для работы ONECLICK@VPN"
published_at: "2026-02-15"
updated_at: ""
tags: ["xkeen", "keenetic", "windows", "entware", "xray", "router", "весь дом"]
category: "help"
reading_time_minutes: 12
---

# Настройка XKeen с помощью Windows

Полная и подробная инструкция по настройке XKeen на роутерах Keenetic в Windows.

Инструкция может показаться объемной, но она структурирована и включает все необходимые шаги для установки и настройки утилиты XKeen на роутере Keenetic.

В процессе вам потребуется USB-накопитель, который будет использоваться как постоянное хранилище для компонентов системы. Далее вы настроите сам роутер: установите необходимые компоненты, пропишете параметры DNS и выполните установку среды Entware. Через SSH-подключение вы установите утилиту XKeen.

Затем вы замените конфигурационные файлы Xray на персонализированные с учетом используемого VPN-сервера и ваших предпочтений. В завершение вы обновите ядро Xray до актуальной версии и запустите систему.

Инструкция сопровождается скриншотами и видео на каждом ключевом этапе. Следуйте ей последовательно и внимательно — это обеспечит стабильную и безопасную работу VPN на вашем устройстве.

Установить утилиту возможно только на роутеры с USB портом. В других моделях недостаточно внутренней памяти для корректной работы.

<div style="margin: 0 20px;">
  <details>
    <summary><strong>Список подходящих роутеров</strong></summary>

- Netcraze Ultra (NC-1812)
- Keenetic Peak (KN-2710)
- Keenetic Ultra (KN-1811)
- Keenetic Giga (KN-1012)
- Keenetic Hopper (KN-3811)
- Keenetic Hopper SE (KN-3812)
- Keenetic 4G (KN-1212)
- Keenetic Skipper 4G (KN-2910)
- Keenetic Omni (KN-1410/1411)
- Keenetic Extra (KN-1710/1711/1713)
- Keenetic Giga (KN-1010/1011)
- Keenetic Ultra (KN-1810)
- Keenetic Viva (KN-1910/1912/1913)
- Keenetic Giant (KN-2610)
- Keenetic Hero 4G (KN-2310/2311)
- Keenetic Hopper (KN-3810)
- Zyxel Keenetic II / III
- Zyxel Keenetic Extra, Extra II
- Zyxel Keenetic Giga II / III
- Zyxel Keenetic Omni, Omni II
- Zyxel Keenetic Viva
- Zyxel Keenetic Ultra, Ultra II
- Keenetic Ultra SE (KN-2510)
- Keenetic Giga SE (KN-2410)
- Keenetic DSL (KN-2010)
- Keenetic Skipper DSL (KN-2112)
- Keenetic Duo (KN-2110)
- Keenetic Hopper DSL (KN-3610)
- Zyxel Keenetic DSL
- Zyxel Keenetic LTE
- Zyxel Keenetic VOX

  </details>
</div>

---

## Подготовка USB-накопителя

Для установки и работы утилиты XKeen необходимо подключить накопитель к роутеру, на котором будет установлено необходимое ПО. Отключать его из роутера нельзя.

### Форматирование USB-накопителя в EXT4 и создание SWAP-раздела

В качестве примера используем условно-бесплатное приложение в ОС Windows для работы с разметкой диска MiniTool Partition Wizard Free Edition или другое аналогичное ПО, предназначенное для работы с физическими дисками.

1. Скачайте и установите программу MiniTool Partition Wizard Free Edition.  
   Выберите язык English → Continue installing free edition → MiniTool Partition Wizard Free.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/e8456e2d72266c50e8dee0ccb361cd0d9c41d14d.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

2. Подключите USB-накопитель к компьютеру.
3. Запустите MiniTool Partition Wizard.
4. Выберите USB-накопитель. Удалите все тома, создайте раздел с файловой системой EXT4 и SWAP-раздел для Linux объемом 512 МБ — 1 ГБ. Подробнее о SWAP см. на сайте производителя Keenetic.
5. Назовите EXT4-том `OPKG`.
6. Отключите накопитель и извлеките.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/4ebd5e951c8aaecd37270bcf306f80a9b9648775.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>
---

## Подготовка роутера Keenetic

### Создание бэкапа

Перед установкой OPKG и XKeen рекомендуем сделать резервную копию прошивки и настроек роутера.

1. Войдите в веб-интерфейс роутера. Стандартный адрес: `192.168.1.1` или `my.keenetic.net`.
2. Выберите **Управление → Параметры системы**.
3. Скачайте файлы **firmware** и **startup-config**.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 0 20px;">
  <img src="https://blancvpn.cx/san-cdn/images/jd0fxfd9/production/8a71e30b822cc7a0037baf4d9d65c34485bdf38f-1920x912.png" alt="terminal" style="display:block; width:100%; height:auto;">
</div>

### Установка необходимых компонентов

Далее установите необходимые компоненты Keenetic для работы утилиты XKeen.

1. Подключите подготовленный USB-накопитель к роутеру.
2. Перейдите в **Управление → Параметры системы → Изменить набор компонентов** и установите следующие компоненты:

   - Интерфейс USB
   - Файловая система Ext
   - Общий доступ к файлам и принтерам по протоколу SMB
   - Поддержка открытых пакетов
   - Прокси-сервер DNS-over-TLS
   - Прокси-сервер DNS-over-HTTPS
   - Протокол IPv6
   - Модули ядра подсистемы Netfilter

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 0 20px;">
  <img src="https://blancvpn.cx/san-cdn/images/jd0fxfd9/production/3849760e54c14063b566a42e09e89458fd4b8139-991x1564.png" alt="terminal" style="display:block; width:100%; height:auto;">
</div>

---

## Настройка DNS

### Добавление DNS-записей

1. Нажмите на шестеренку справа вверху страницы конфигуратора и выберите **командную строку**.
2. Введите поочередно команды ниже.

То есть в поле **Command** вводите `dns-proxy`, нажимаете **Send request** и так далее по одной строчке:

```
dns-proxy
```
```
tls upstream 8.8.8.8 sni dns.google
```
```
tls upstream 8.8.4.4 sni dns.google
```
```
tls upstream 1.1.1.1 sni cloudflare-dns.com
```
```
tls upstream 1.0.0.1 sni cloudflare-dns.com
```
```
https upstream https://cloudflare-dns.com/dns-query dnsm
```
```
https upstream https://one.one.one.one/dns-query dnsm
```
```
https upstream https://dns.google/dns-query dnsm
```
```
exit
```
```
system configuration save
```

Готовый список будет выглядеть примерно так:

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/b41bb505e18b0e6353bb33aff4d9a77572929109.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

3. Перезагрузите роутер: **Управление → Параметры системы → Перезагрузка системы → Перезагрузить**.

### Отключение IPv6

1. Перейдите на страницу подключения к Интернету: **Интернет → Кабель Ethernet → Подключения к интернету по Ethernet-кабелю → Порты и VLAN'ы**.
2. Переключите параметр **IPv6** в режим **Не используется**.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 0 20px;">
  <img src="https://blancvpn.cx/san-cdn/images/jd0fxfd9/production/1c6443a8b4d2d444752b412ac1505f5c747e1633-3240x1900.png" alt="terminal" style="display:block; width:100%; height:auto;">
</div>

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #9CA3AF;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  После сохранения настроек вы автоматически переподключитесь к Интернету.
</div>

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #EF4444;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  Перед тем как игнорировать DNS, предоставленный вашим провайдером, убедитесь, что в настройках отсутствуют доменные имена серверов, авторизующих ваше подключение.
  Подробнее см. на <a href="#">сайте производителя</a>.
</div>

---

## Настройка Keenetic для работы с XKeen

### Настройка политики доступа в Интернет

Для корректной работы XKeen необходимо настроить маршрутизацию трафика через определенную политику доступа в Интернет на роутере Keenetic.

Политика доступа определяет, через какого провайдера или интернет-канал будет идти трафик: VPN или напрямую от провайдера. XKeen работает как прокси-клиент, который должен быть привязан к конкретной политике, чтобы ваши устройства могли использовать VPN.

1. **Создание политики XKeen:**
   - В веб-интерфейсе роутера выберите **Интернет → Приоритеты подключений → Политики доступа в интернет**.
   - Создайте новую политику с названием **XKeen**.
   - При наличии нескольких провайдеров можно включить **Многопутевую передачу** для повышения надежности соединения.
   - Активируйте галочку для **Ethernet-подключения**.
   - Нажмите **Сохранить**.

2. **Назначение устройств для политики:**
   - Выберите **Приоритеты подключений → Применение политик**.
   - Добавьте в созданную политику нужные устройства:
     - **Клиент** — отдельные устройства в вашей сети (ПК, смартфоны, ТВ).
     - **Сеть** — все устройства в определенном сегменте сети
   - Нажмите **Сохранить**.

После настройки политики все устройства, добавленные в нее, будут использовать VPN XKeen для доступа в Интернет согласно настроенным правилам маршрутизации.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/4af08a67a5134445b16881642e97fdc24095c0c8.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

### Перенос сервисов Keenetic с порта 443

Порт 443 обычно занят сервисами Keenetic. Перенос позволяет избежать конфликта.

После переноса сервисы Keenetic, такие как KeenDNS, будут доступны по новому порту. Например, если вы перенесли сервисы с 443 на 8443, доступ к KeenDNS будет осуществляться по адресу `xxxx.keenetic.link:8443`.

Рекомендуемые порты для переноса: 5083, 5443, 8083, 8443 или 65083.

1. Перейдите в раздел **Управление → Пользователи и доступ**.
2. Найдите параметр **Порт управление по HTTPS**.
3. Смените порт с 443 на 8443.
4. Сохраните.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/2685e939cb3a1c4c61345ff0c273f37b7660839d.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

---

## Установка Entware

Entware — это репозиторий программного обеспечения для устройств с ограниченными ресурсами, таких как роутеры Keenetic. Он позволяет устанавливать дополнительные приложения на внешний USB-накопитель, расширяя возможности роутера без изменения его основной прошивки. В контексте XKeen Entware необходим как основа для установки и работы программного обеспечения, включая сам XRay, библиотеки и утилиты для работы с ним.

### Подготовка установочных файлов

1. Скачайте архив установщика Entware, соответствующий вашей модели роутера.

<div style="margin: 0 20px;">
  <details>
    <summary><strong>Справка по моделям роутера</strong></summary>

Для более новых моделей с KeeneticOS 4.0 и выше почти всегда следует использовать версию для aarch64, так как они используют более современные процессоры на архитектуре ARM.

**Для моделей с процессором aarch64 (используйте aarch64-installer.tar.gz):**
- Keenetic Peak (KN-2710)
- Keenetic Ultra (KN-1811)
- Keenetic Giga (KN-1012)
- Keenetic Hopper (KN-3811)
- Keenetic Hopper SE (KN-3812)

**Для моделей с процессором mipsel (используйте mipsel-installer.tar.gz):**
- Keenetic 4G (KN-1212)
- Keenetic Skipper 4G (KN-2910)
- Keenetic Omni (KN-1410/1411)
- Keenetic Extra (KN-1710/1711/1713)
- Keenetic Giga (KN-1010/1011)
- Keenetic Ultra (KN-1810)
- Keenetic Viva (KN-1910/1912/1913)
- Keenetic Giant (KN-2610)
- Keenetic Hero 4G (KN-2310/2311)
- Keenetic Hopper (KN-3810)
- Zyxel Keenetic II / III
- Zyxel Keenetic Extra, Extra II
- Zyxel Keenetic Giga II / III
- Zyxel Keenetic Omni, Omni II
- Zyxel Keenetic Viva
- Zyxel Keenetic Ultra, Ultra II

**Для моделей с процессором mips (используйте mips-installer.tar.gz):**
- Keenetic Ultra SE (KN-2510)
- Keenetic Giga SE (KN-2410)
- Keenetic DSL (KN-2010)
- Keenetic Skipper DSL (KN-2112)
- Keenetic Duo (KN-2110)
- Keenetic Hopper DSL (KN-3610)
- Zyxel Keenetic DSL
- Zyxel Keenetic LTE
- Zyxel Keenetic VOX

На моделях Keenetic Skipper 4G (KN-2910) и Keenetic 4G (KN-1212) требуется ручная замена ядра. Напишите в поддержку, мы вышлем актуальную версию: https://t.me/vpn_oneclick

  </details>
</div>

2. Создайте на отформатированном USB-накопителе папку `install` с помощью приложения **Диски и принтеры** в веб-конфигураторе.
3. Поместите скачанный архив `…installer.tar.gz` в папку `install` на USB-накопителе.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/220de8ecebbe93cc42327c7229ede026a42e1326.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

### Установка Entware

1. Перейдите в раздел **OPKG**.
2. В поле **Накопитель** выберите USB-накопитель.
3. Сценарий `initrc` должен оставаться пустым. В процессе завершения установки он будет автоматически изменен на `/opt/etc/init.d/rc.unslung`.
4. Нажмите **Сохранить**.
5. Подождите несколько минут, пока установятся все пакеты Entware [5/5]. Отследить процесс установки можно в системном журнале роутера.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/ba5737af8467592dfc1a0ca523266f6e8154bcfb.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

---

## Подключение к Entware через SSH

### Установка PuTTY

Это программа-клиент для удаленного доступа к устройствам через протоколы SSH и Telnet. Они позволяют подключаться к роутеру или серверу через командную строку и выполнять настройку без использования веб-интерфейса. PuTTY — бесплатная классическая программа для Windows.

Скачайте и установите программу PuTTY с сайта.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/260f890c80904be78ff22b71cfbda0c1e19949dc.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

### Подключение к Entware через PuTTY

Выберите параметры для подключения.

1. Host Name: по умолчанию (`192.168.1.1`)

<div style="margin: 0 20px;">
  <details>
    <summary><strong>Как узнать IP-адрес роутера</strong></summary>

Ранее адрес был указан в адресной строке браузера при подключении к веб-конфигуратору роутера. Также можно посмотреть на наклейку с обратной стороны роутера.

Или в интерфейсе устройства: выберите пункт Wi-Fi или Сеть и интернет. Затем откройте Wi-Fi-сеть, к которой вы подключены. В информации о сети перейдите в раздел Детали или Дополнительно. Здесь будут данные о сети, включая IP-адрес роутера.

  </details>
</div>


2. Port: `22`  
   <div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #9CA3AF;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  Используйте порт 22, если не установлен компонент Сервер SSH. Если установлен — используйте порт 222.

</div>
3. Connection type: `SSH`
4. Нажмите Open и подтвердите добавление ключа безопасности, нажав **Accept**.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/ba5737af8467592dfc1a0ca523266f6e8154bcfb.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

### Смените пароль

После подключения по SSH через программу PuTTY у вас откроется черное окно терминала по управлению утилитой XKeen.

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #9CA3AF;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  Команды можно вставлять правой кнопкой мыши.
</div>

1. Введите логин (login as): `root`
2. Введите стандартный пароль (password): `keenetic`

После входа по SSH вы увидите информацию об оболочке BusyBox v1.37.0.

3. Выполните команду `passwd`
4. Придумайте пароль (можно воспользоваться любым генератором паролей).
5. Введите новый пароль дважды:
   - New password: `введите новый пароль`
   - Retype password: `повторите пароль`

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #9CA3AF;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  При вводе пароля символы не отображаются — это нормально. Просто вставьте или вводите пароль и нажмите Enter.
</div>

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #22C55E;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  Запомните или запишите данные логина (root) и новый пароль для будущих подключений.

</div>
Если что-то пошло не так, подключитесь по SSH заново.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/ca2354227d038f3960e0a1e1a87a4c6549735061.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

---

## Установка XKeen

Для установки XKeen выполните действия в PuTTY:

1. Обновите список пакетов:

```
opkg update && opkg upgrade && opkg install curl tar
```

2. Загрузите установочный скрипт XKeen:

```
curl -OL https://raw.githubusercontent.com/jameszeroX/XKeen/main/install.sh
```

3. Сделайте скрипт исполняемым:

```
chmod +x ./install.sh
```

4. Запустите установочный скрипт:

```
./install.sh
```

Во время установки вам потребуется выбрать компоненты и настроить расписание их автоматического обновления.

1. Когда появится меню установки, выберите ядро проксирования Xray: `1`.
2. Затем актуальную версию ядра: `1`.
3. После этого выберите `1`. Установить отсутствующие GeoSite.
4. Затем выберите `1`. Установить отсутствующие GeoIP.
5. Включите обновление GeoFile: `1`. Включить задачу.
6. Задайте расписание обновлений (например, `1 → 23 → 30`).
7. Добавьте XKeen в автозагрузку: `1`.

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/7e452ba632e70144a695e68fbfc4ce0fdd8a0324.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #9CA3AF;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:18px 20px 0;
">
  Не закрывайте окно PuTTY. После настройки файлов нужно будет ввести еще одну команду.
</div>

---

## Настройка Xray в XKeen

Необходимо заменить существующие файлы конфигурации на ваши. XKeen требует настройки трех основных конфигурационных файлов, которые определяют работу Xray:

1. `03_inbounds.json` — определяет, как входящий трафик будет попадать в Xray.
2. `04_outbounds.json` — настраивает подключение к VPN-серверу.
3. `05_routing.json` — содержит правила маршрутизации трафика.

---

## Получение файлов конфигураций для настройки XKeen

### Настройка входящего трафика [inbounds]

Файл `03_inbounds.json` определяет, как входящий трафик поступает в Xray для обработки. Это ключевой конфигурационный файл, который настраивает входные точки для трафика в системе XKeen.

Его достаточно скачать по [ссылке](https://github.com/Corvus-Malus/XKeen/releases/latest/download/03_inbounds.json).

### Настройка подключения к VPN-серверу [outbounds]

Файл `04_outbounds.json` определяет, куда и как XKeen будет направлять трафик после его обработки. То есть какой VPN-сервер будет подключен.

**Файл `04_outbounds.json` выдаётся в поддержке ONECLICK@VPN:** https://t.me/vpn_oneclick

### Настройка маршрутизации [routing]

Маршрутизация — ключевая функция XKeen, которая позволяет выборочно направлять трафик через VPN, напрямую через провайдера или блокировать его. Все настройки маршрутизации задаются в файле `05_routing.json`.

[VPN для всех сайтов](https://raw.githubusercontent.com/ValeriiOsodoev/VPN_ADM/refs/heads/main/VPN%20%D0%B4%D0%BB%D1%8F%20%D0%B2%D1%81%D0%B5%D1%85%20%D1%81%D0%B0%D0%B8%CC%86%D1%82%D0%BE%D0%B2.json?token=GHSAT0AAAAAADI2VJDVZTJIE5NQZ4U5UQBI2MS735Q).

[VPN для всех сайтов кроме России](https://raw.githubusercontent.com/ValeriiOsodoev/VPN_ADM/refs/heads/main/VPN%20%D0%B4%D0%BB%D1%8F%20%D0%B2%D1%81%D0%B5%D1%85%20%D1%81%D0%B0%D0%B8%CC%86%D1%82%D0%BE%D0%B2%2C%20%D0%BA%D1%80%D0%BE%D0%BC%D0%B5%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8.json?token=GHSAT0AAAAAADI2VJDU2RAMC6A2U2ZYX5LS2MS74PQ).

[VPN для сайтов из базы заблокированных](https://raw.githubusercontent.com/ValeriiOsodoev/VPN_ADM/refs/heads/main/VPN%20%D0%B4%D0%BB%D1%8F%20%D1%81%D0%B0%D0%B8%CC%86%D1%82%D0%BE%D0%B2%20%D0%B8%D0%B7%20%D0%B1%D0%B0%D0%B7%D1%8B%20%D0%B7%D0%B0%D0%B1%D0%BB%D0%BE%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.json?token=GHSAT0AAAAAADI2VJDVUOD5R77UWCOURGWS2MS74YQ).

Мы рекомендуем выбрать вариант “VPN для сайтов из базы заблокированных”. При необходимости вы можете настроить правила под себя (домены, IP и т.д.) и использовать расширенные настройки.

**Если хотите более "тонкую" настройку маршрутизации - обратитесь в поддержку ONECLICK@VPN:** https://t.me/vpn_oneclick

---

## Замена файлов

Замените все три файла `03_inbounds.json`, `04_outbounds.json`, `05_routing.json` на полученные выше. Для этого через роутер откройте нужную папку на накопителе и загрузите файлы, после чего подтвердите замену.

1. В веб-конфигураторе откройте USB-накопитель: **Управление → Приложения → Диски и принтеры → ваш USB-накопитель**.
2. Перейдите в директорию `OPKG/etc/xray/configs/`.
3. Загрузите файлы в эту директорию и замените существующие шаблоны на ваши.

<div style="
  border:1px solid #E5E7EB;
  border-left:8px solid #EF4444;
  border-radius:14px;
  padding:18px 20px;
  background:#F9FAFB;
  font-size:16px;
  line-height:1.35;
  color:#111827;
  margin:0 20px;
">
  При каждой следующей замене файлов `03_inbounds.json`, `04_outbounds.json` или `05_routing.json` нужно перезапускать XKeen командой `xkeen -restart`, чтобы изменения вступили в силу.
</div>

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 18px 20px 0;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/2575fa6f177cce3411619bb42f545d9d2251b98d.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

---

## Оптимизация

Для снижения нагрузки на процессор также ограничим работу XKeen портами 80, 443 и 50000:50030:

Выполните эту команду, чтобы ограничить работу портов:

```
xkeen -ap 80,443,50000:50030
```

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 0 20px;">
  <video
    src="https://blancvpn.cx/san-cdn/files/jd0fxfd9/production/901eb12f1bcfb54d9d38c76ee6fb813b59e860ff.mp4#t=0.001"
    controls
    style="display:block; width:100%; height:auto;">
  </video>
</div>

У вас прокси-клиент не будет запущен на этом этапе.

---

## Запуск

Запустите XKeen командой `xkeen -start`

<div style="border-radius:24px; overflow:hidden; box-shadow:0 20px 60px rgba(0,0,0,.35); display:inline-block; margin: 0 20px;">
  <img src="https://blancvpn.cx/san-cdn/images/jd0fxfd9/production/762e5c08c89b66974f141b7612535a9f7552dd37-1896x755.png" alt="terminal" style="display:block; width:100%; height:auto;">
</div>

---

Готово! Теперь на вашем роутере настроен продвинутый VPN персонально под вас.

Если у вас возникнут какие-либо проблемы, свяжитесь с нашей службой поддержки или напишите в телеграм-чат сообщества. Мы всегда готовы помочь!

---

## Нужна помощь?

Написать в поддержку: https://t.me/vpn_oneclick
