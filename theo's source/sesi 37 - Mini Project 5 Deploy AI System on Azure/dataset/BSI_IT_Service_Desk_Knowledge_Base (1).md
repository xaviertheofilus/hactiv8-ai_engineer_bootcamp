# KUMPULAN STANDARD OPERATING PROCEDURE (SOP) 
## BSI IT SERVICE DESK - MITSUBISHI INDONESIA

**Dokumen Master Knowledge Base untuk AI Assistant & IT Helpdesk Agent**
**Versi:** 1.0 (Comprehensive RAG Knowledge Base)
**Klasifikasi:** Internal Use Only
**Target Audiens:** BSI IT Helpdesk Agents (Level 1 & Level 2)

---

## DAFTAR ISI
1. SOP-001: Panduan Instalasi dan Troubleshooting VPN FortiClient
2. SOP-002: Reset Token MFA (Multi-Factor Authentication)
3. SOP-003: Active Directory Password Reset
4. SOP-004: SAP GUI Login Issues & Account Unlock
5. SOP-005: SAP Transaction Errors & Authorization (SU53)
6. SOP-006: Outlook & Microsoft Exchange Email Issues
7. SOP-007: Network Printer Setup & Troubleshooting
8. SOP-008: Laptop & Hardware Request (Pengadaan Baru/Penggantian)
9. SOP-009: Software Installation Request & Licensing
10. SOP-010: New Employee Onboarding (IT Provisioning)
11. SOP-011: Employee Account Termination & Offboarding
12. SOP-012: Microsoft Teams & M365 Access Management
13. SOP-013: Corporate WiFi Access & 802.1x Authentication

---

<a id="sop-001"></a>
## SOP-001: PANDUAN INSTALASI DAN TROUBLESHOOTING VPN FORTICLIENT

### 1. Tujuan dan Ruang Lingkup
Prosedur ini menjelaskan langkah-langkah untuk membantu pengguna (karyawan Mitsubishi Indonesia) menginstal, mengonfigurasi, dan memecahkan masalah koneksi VPN (Virtual Private Network) menggunakan FortiClient. Akses VPN diwajibkan untuk mengakses sistem internal seperti SAP dan File Server saat bekerja secara remote (Work From Home/Anywhere).

### 2. SLA (Service Level Agreement)
- **Tingkat Prioritas:** Medium - High (Jika berdampak pada operasional kritis)
- **Waktu Respon (SLA):** 15 menit
- **Waktu Penyelesaian (SLA):** 2 jam

### 3. Prasyarat Sistem
- Laptop/PC dengan OS Windows 10/11 atau macOS 12+ (sudah terdaftar di Intune/SCCM).
- Koneksi internet stabil (minimal 5 Mbps).
- Akun Active Directory (AD) pengguna dalam status aktif.
- Perangkat sudah di-assign grup keamanan `VPN-Remote-Access` di Entra ID.

### 4. Langkah-Langkah Instalasi & Konfigurasi
1. **Download Installer:** Arahkan pengguna ke portal internal (https://software.mitsubishi.co.id/forticlient) atau gunakan *Software Center* (Windows).
2. **Instalasi:** Jalankan installer dengan hak akses Administrator (Jika pengguna tidak memiliki hak admin, bantu menggunakan LAPS via remote session).
3. **Konfigurasi Koneksi Baru:**
   - Buka FortiClient.
   - Klik **Configure VPN**.
   - Connection Name: `Mitsubishi Corp VPN`
   - Description: `Remote Access BSI`
   - Remote Gateway: `vpn.mitsubishi.co.id`
   - Port: `443` (atau `10443` sebagai alternatif jika port 443 diblokir oleh ISP lokal pengguna).
   - Centang opsi **Enable Single Sign On (SSO) for VPN Tunnel**.
4. **Login:** Gunakan kredensial Microsoft 365 pengguna (UPN/Email dan Password) dan setujui prompt MFA di ponsel.

### 5. Panduan Troubleshooting (L1 Helpdesk)
**Skenario A: Error "Credential or SSL VPN Configuration is wrong" (-14)**
- **Penyebab:** Salah password, akun terkuci, atau pengguna belum masuk grup VPN.
- **Tindakan Agen:**
  1. Verifikasi status akun AD di Active Directory Users and Computers (ADUC). Buka kunci jika *Locked Out*.
  2. Pastikan pengguna ada di grup `VPN-Remote-Access`. Jika tidak ada, minta persetujuan manajer dan tambahkan.

**Skenario B: Koneksi tersambung tetapi di putus pada 40% atau 80%**
- **Penyebab:** Masalah sertifikat mesin atau ISP memblokir protokol IPsec/SSL tertentu.
- **Tindakan Agen:**
  1. Ubah setting transport dari `IPsec` ke `SSL VPN` (jika menggunakan client versi penuh).
  2. Bersihkan cache TLS di Windows: Buka `inetcpl.cpl` -> Tab *Advanced* -> *Restore advanced settings*.

**Skenario C: VPN Terhubung tetapi tidak bisa akses SAP/Intranet**
- **Penyebab:** Routing issue atau DNS tidak ter-resolve.
- **Tindakan Agen:** Buka Command Prompt, jalankan `ipconfig /flushdns`. Ping ke `sap-prod.mitsubishi.local`. Jika RTO, eskalasi ke L2 Network.

### 6. Matriks Eskalasi
- **Eskalasi ke:** Level 2 Network Security Team.
- **Informasi yang dibutuhkan:** Username, IP Public Pengguna, Log FortiClient (Ekspor ke file .txt), Timestamp kejadian.

---

<a id="sop-002"></a>
## SOP-002: RESET TOKEN MFA (MULTI-FACTOR AUTHENTICATION)

### 1. Tujuan dan Ruang Lingkup
Mengatur prosedur verifikasi dan reset token MFA (Microsoft Authenticator) untuk pengguna yang kehilangan ponsel, mengganti nomor HP, atau tidak sengaja menghapus aplikasi Authenticator. Keamanan sangat ketat di sini untuk mencegah serangan *Social Engineering*.

### 2. SLA (Service Level Agreement)
- **Tingkat Prioritas:** High (Pemblokiran total akses kerja)
- **Waktu Respon:** 10 menit
- **Waktu Penyelesaian:** 30 menit

### 3. Kebijakan Keamanan (Wajib Dibaca Agen)
**PERINGATAN:** Agen dilarang keras mereset MFA hanya berdasarkan permintaan via Email atau Chat tanpa verifikasi identitas visual atau suara. 

### 4. Langkah Verifikasi Identitas
Pilih salah satu metode berikut sebelum melakukan reset:
1. **Panggilan Video (Teams/Zoom):** Minta pengguna menyalakan kamera dan tunjukkan ID Card/Badge karyawan Mitsubishi.
2. **Verifikasi via Manajer (Direkomendasikan):** Hubungi langsung atasan pengguna (Manager yang tertera di Workday/AD) melalui Teams Chat/Call, tanyakan: "Apakah benar staf Anda bernama [Nama] meminta reset MFA karena ganti HP?"
3. **Verifikasi Data Rahasia:** Tanyakan NIK (Nomor Induk Karyawan), Tanggal Lahir, dan Departemen.

### 5. Prosedur Reset di Entra ID (Azure AD)
1. Login ke [Entra ID Admin Center] (https://entra.microsoft.com).
2. Navigasi ke **Users** > **All users**.
3. Cari nama pengguna atau UPN (Email).
4. Klik pada profil pengguna.
5. Di menu sebelah kiri, pilih **Authentication methods**.
6. Klik **Require re-register multifactor authentication**.
7. Hapus (Delete) perangkat lama yang terdaftar di daftar metode autentikasi.
8. Beritahu pengguna: "MFA Anda telah direset. Silakan buka browser dalam mode Incognito, akses portal.office.com, login menggunakan email dan password Anda. Layar akan meminta Anda untuk mengatur ulang Microsoft Authenticator."

### 6. Template Balasan ke Pengguna
*Halo [Nama Pengguna],
Sesuai verifikasi dengan manajer Anda, kami telah melakukan reset sesi Multi-Factor Authentication (MFA) pada akun Anda.
Mohon siapkan aplikasi Microsoft Authenticator di smartphone baru Anda, lalu login ke office.com dari PC untuk melakukan proses pairing ulang melalui scan QR Code.
Jika ada kendala, balas email ini. Terima kasih.*

---

<a id="sop-003"></a>
## SOP-003: ACTIVE DIRECTORY PASSWORD RESET

### 1. Tujuan dan Ruang Lingkup
Dokumen ini menjadi acuan bagi agen Service Desk dalam menangani tiket *Password Reset* dan *Account Unlock* untuk domain `mitsubishi.local` dan Entra ID.

### 2. Kebijakan Kata Sandi (Password Policy)
- Minimal 12 karakter.
- Harus mengandung minimal 3 dari 4 kriteria: Huruf besar, Huruf kecil, Angka, Karakter Spesial (!@#$%^&*).
- Tidak boleh sama dengan 5 password terakhir.
- Tidak boleh mengandung nama depan atau nama belakang pengguna.
- Expire setiap 90 hari.

### 3. Self-Service Password Reset (SSPR)
Langkah pertama yang **harus** agen lakukan adalah mengedukasi pengguna menggunakan SSPR:
1. Arahkan pengguna ke: `https://passwordreset.microsoftonline.com/`
2. Minta pengguna memasukkan email dan mengisi *Captcha*.
3. Pengguna memilih metode verifikasi: SMS ke nomor HP terdaftar atau Approval via Microsoft Authenticator.
4. Jika pengguna gagal karena MFA belum terdaftar/HP hilang, agen dapat melakukan reset manual.

### 4. Prosedur Reset Manual oleh Agen (BSI IT)
Jika SSPR tidak memungkinkan:
1. Buka console **Active Directory Users and Computers (ADUC)**.
2. Cari user pada OU yang bersangkutan (Gunakan fitur *Find*).
3. Klik kanan pada user -> pilih **Reset Password**.
4. Masukkan *Temporary Password* dengan standar format perusahaan: `Mitsu[Bulan][Tahun]!@#` (contoh: `MitsuAgustus2026!@#`).
5. **WAJIB CENTANG:** "User must change password at next logon".
6. Jika akun juga terkunci, centang "Unlock the user's account".
7. Berikan temporary password kepada pengguna via jalur komunikasi aman (telepon atau chat ke atasan, JANGAN kirim via email ke email personal pengguna kecuali disetujui HR).

---

<a id="sop-004"></a>
## SOP-004: SAP GUI LOGIN ISSUES & ACCOUNT UNLOCK

### 1. Tujuan
Membantu pengguna yang mengalami kegagalan login ke aplikasi SAP ERP (SAP Logon / SAP GUI). Catatan penting: Sistem autentikasi SAP di Mitsubishi Indonesia saat ini **belum** terintegrasi penuh dengan SSO (Single Sign-On) Active Directory untuk semua sistem (Production vs QA/Dev).

### 2. Identifikasi Masalah Utama
Tanyakan kepada pengguna pesan error yang muncul di layar bagian bawah (Status bar SAP).
1. Error: *"Password logon no longer possible - too many failed attempts"* (Akun Terkunci)
2. Error: *"Logon data incorrect (check client, user and password)"* (Salah Password/Client)
3. Error: *"User is locked by administrator"* (Akun di-lock manual oleh basis/audit)

### 3. Prosedur Penyelesaian (Tindakan Agen Helpdesk)
Karena agen L1 BSI Helpdesk memiliki akses modul SU01 (Display & Password Reset) di sistem PRD (Production):

**A. Unlock Akun (Kunci karena salah password 3x):**
1. Buka aplikasi SAP Logon dan masuk ke sistem yang diminta (contoh: P01 - Production).
2. Jalankan T-Code: `SU01`.
3. Masukkan SAP User ID pengguna.
4. Klik ikon **Lock/Unlock** (Gambar gembok).
5. Sistem akan menunjukkan apakah akun terkunci karena *"incorrect logons"*.
6. Klik tombol **Unlock**. Informasikan pengguna untuk mencoba kembali dengan password lama mereka.

**B. Reset Password SAP:**
1. Jalankan T-Code: `SU01`.
2. Masukkan SAP User ID.
3. Klik ikon **Logon Data / Password** (Gambar kunci).
4. Masukkan *Initial Password* standar: `Init123456!`.
5. Klik **Save** (Gambar disket).
6. Beritahu pengguna: "Password SAP Anda telah di-reset ke `Init123456!`. Pastikan Anda memasukkan nomor Client yang benar (misal: 100). Saat login, SAP akan langsung meminta Anda membuat password baru."

### 4. Eskalasi ke SAP Basis
Eskalasi ke grup tiket `SAP_Basis_L2` jika:
- Pesan error adalah *"User is not authorized for system"*.
- Pengguna butuh akses ke sistem Development (D01) atau Quality (Q01) di mana agen L1 tidak memiliki akses SU01.

---

<a id="sop-005"></a>
## SOP-005: SAP TRANSACTION ERRORS & AUTHORIZATION (SU53)

### 1. Tujuan
Menangani tiket pengguna yang mengeluh tidak dapat mengakses menu tertentu di SAP (contoh: tidak bisa buat PO di ME21N, tidak bisa lihat laporan keuangan di FBL3N).

### 2. SLA (Service Level Agreement)
- **Prioritas:** Medium
- **Waktu Penyelesaian:** 1 - 2 Hari Kerja (karena butuh approval pemilik bisnis/Business Process Owner).

### 3. Analisis Awal (SU53 Report)
BSI IT Helpdesk **tidak diperbolehkan** langsung menambahkan role ke akun SAP pengguna. Semua penambahan role harus melalui audit trail.
1. Saat pengguna melapor error "You are not authorized to use transaction XXXX", instruksikan pengguna untuk tidak menutup layar SAP mereka.
2. Minta pengguna mengetik `//SU53` di kotak perintah (command field) pada jendela SAP yang sama, lalu tekan Enter.
3. Layar akan menampilkan laporan **Authorization Failure**.
4. Minta pengguna mengambil *screenshot* (tangkapan layar) layar penuh SU53 tersebut dan melampirkannya ke dalam tiket IT Service Desk.

### 4. Prosedur Eskalasi & Role Assignment
1. Verifikasi kelengkapan screenshot SU53.
2. Periksa apakah pengguna sudah melampirkan email persetujuan dari *Business Process Owner (BPO)* atau Manager Departemen terkait.
3. Jika persetujuan belum ada, balas tiket:
   *Mohon lampirkan persetujuan (approval) dari Manager Anda dan BPO modul terkait (misal BPO Finance/HR/Supply Chain) untuk penambahan hak akses T-Code tersebut.*
4. Jika persetujuan sudah lengkap, teruskan tiket ke tim `SAP_Security_Admin`.
5. **Format Catatan Tiket Eskalasi:**
   - User ID: [User ID]
   - Missing T-Code/Auth Object: [Dari Screenshot SU53]
   - Approval: [Tautan atau Attachment Email]

---

<a id="sop-006"></a>
## SOP-006: OUTLOOK & MICROSOFT EXCHANGE EMAIL ISSUES

### 1. Tujuan
Menyelesaikan berbagai kendala terkait layanan email Microsoft Outlook (Desktop App) dan Exchange Online.

### 2. Masalah Umum 1: Outlook "Disconnected" atau "Trying to Connect"
**Langkah Troubleshooting:**
1. Pastikan koneksi internet aktif. Jika WFH, pastikan VPN tersambung jika mengakses resource internal, walaupun Exchange M365 tidak wajib VPN.
2. Cek status server Microsoft 365 di portal admin (Apakah ada *Global Outage*?).
3. Restart aplikasi Outlook.
4. Jika persisten, gunakan tool **Microsoft Support and Recovery Assistant (SaRA)**.
5. Jika masalahnya cache, lakukan *Rebuild OST file*:
   - Tutup Outlook.
   - Buka `C:\Users\<username>\AppData\Local\Microsoft\Outlook`
   - Ubah nama file `<email>.ost` menjadi `<email>.ost.old`.
   - Buka kembali Outlook dan biarkan mengunduh ulang email (bisa memakan waktu lama, pastikan terhubung WiFi kencang).

### 3. Masalah Umum 2: Mailbox Full / Kuota Habis (Error 5.2.2)
Mitsubishi menggunakan lisensi E3 (100GB kuota utama).
**Tindakan:**
1. Edukasi pengguna untuk mengaktifkan **Online Archive**.
2. Jika fitur belum aktif, agen login ke Exchange Admin Center.
3. Cari akun pengguna -> **Mailbox features** -> **Mailbox archive** -> Set to *Enabled*.
4. Instruksikan pengguna membuat *Retention Policy* lokal di Outlook untuk memindahkan email lama (>1 tahun) ke *Online Archive* secara otomatis.

### 4. Masalah Umum 3: Outlook Search Tidak Berfungsi
- Buka Control Panel -> Indexing Options -> klik *Advanced* -> klik **Rebuild**.
- Peringatkan pengguna bahwa proses rebuild dapat memakan waktu beberapa jam dan performa laptop mungkin sedikit menurun selama proses.

---

<a id="sop-007"></a>
## SOP-007: NETWORK PRINTER SETUP & TROUBLESHOOTING

### 1. Tujuan
Panduan instalasi printer jaringan kantor dan penanganan gagal *print*. Lingkungan Mitsubishi menggunakan arsitektur Print Server terpusat.

### 2. Cara Mapping Printer Baru (Windows 10/11)
1. Pastikan pengguna berada di jaringan kantor (Kabel LAN atau Corporate WiFi). Jika WFH (VPN), pencetakan langsung ke kantor umumnya diblokir kecuali ada pengecualian IP.
2. Tekan tombol `Windows + R`, ketik alamat print server lokal berdasarkan cabang, contoh:
   - Head Office (Jakarta): `\print-jkt.mitsubishi.local`
   - Pabrik (Cikarang): `\print-ckr.mitsubishi.local`
3. Tekan Enter. Jendela Explorer berisi daftar printer akan muncul.
4. Cari nama printer yang tertera di stiker fisik printer (misal: `PRT-JKT-FLOOR5-COLOR`).
5. Klik kanan pada printer tersebut dan pilih **Connect**.
6. Driver akan terunduh dan terinstal secara otomatis.
7. Buka Control Panel -> *Devices and Printers* -> Set sebagai *Default Printer* jika diminta.

### 3. Troubleshooting "Print Job Stuck" (Nyangkut)
Jika dokumen dikirim namun tidak tercetak:
1. Minta pengguna membatalkan (cancel) semua job di antrean printer komputer mereka.
2. *Clear Print Spooler* di PC pengguna:
   - Buka *Command Prompt* sebagai Administrator.
   - Ketik: `net stop spooler`
   - Hapus file di `C:\Windows\System32\spool\PRINTERS`
   - Ketik: `net start spooler`
3. Jika masih gagal, cek status LCD fisik printer (Apakah kertas habis? Apakah ada *Paper Jam*? Apakah indikator tinta/toner merah?).
4. Eskalasikan ke tim *IT Support Onsite* (L2) untuk pengecekan fisik jika masalah bukan pada OS/Jaringan.

---

<a id="sop-008"></a>
## SOP-008: LAPTOP & HARDWARE REQUEST

### 1. Tujuan
Menstandarkan proses permintaan laptop baru, penggantian laptop rusak, atau permintaan aksesori tambahan (Monitor, Headset, Docking).

### 2. Kategori Permintaan
- **New Hire (Karyawan Baru):** Akan di-trigger otomatis oleh sistem Workday HR 7 hari sebelum tanggal bergabung.
- **Refresh/Replacement:** Penggantian laptop yang sudah mencapai umur pakai >4 tahun atau rusak parah.
- **Upgrade/Aksesori:** Permintaan tambahan untuk produktivitas.

### 3. Prosedur (BSI IT Helpdesk)
1. Terima tiket melalui portal IT Service Management (ServiceNow).
2. Verifikasi alasan pengajuan.
3. **Pengecekan Approval:**
   - Untuk aksesori standar (Mouse, Keyboard): Hanya butuh approval Manager langsung.
   - Untuk penggantian/Laptop Baru: Butuh approval Manager Langsung dan IT Asset Manager.
4. **Alokasi Perangkat (Jika Approved):**
   - Teruskan tiket ke tim `IT_Asset_Management`.
   - Tim Aset akan menyiapkan unit (Imaging OS via Autopilot/SCCM).
   - Atur jadwal pengambilan di IT Lounge atau atur pengiriman kurir asuransi jika user di luar kota.
5. **Retur Barang Lama:**
   - Jika ini penggantian (replacement), pengguna **wajib** mengembalikan perangkat lama dalam waktu maksimal 7 hari setelah menerima yang baru. Jika tidak, akun akan ditangguhkan sementara.

---

<a id="sop-009"></a>
## SOP-009: SOFTWARE INSTALLATION REQUEST & LICENSING

### 1. Kebijakan Dasar
Karyawan Mitsubishi **tidak** memiliki hak akses Local Administrator di perangkat mereka. Semua instalasi perangkat lunak harus melalui sistem distribusi manajemen tersentralisasi (Microsoft Endpoint Configuration Manager / Intune) atau dieksekusi IT via PIM (Privileged Identity Management) / LAPS.

### 2. Alur Permintaan (Software Berlisensi vs Gratis)
**Software Standar (Pre-approved / Freeware seperti Adobe Reader, 7-Zip, Google Chrome):**
- Arahkan pengguna ke aplikasi **Software Center** (Windows) atau **Company Portal** di laptop mereka.
- Pengguna dapat mencari dan mengklik "Install" secara mandiri (Self-Service). Tiket dapat langsung ditutup.

**Software Berlisensi (Visio, Project, AutoCAD, Adobe Creative Cloud):**
1. Pengguna membuat tiket "Software Request".
2. Agen Helpdesk wajib mengecek *License Pool* di portal aset perangkat lunak.
3. Minta lampiran *Approval* Manajer dan persetujuan penagihan silang (Cross-Charge) dari Departemen Keuangan jika lisensi harus dibeli baru.
4. Jika disetujui, assign tiket ke grup `IT_Endpoint_Management` untuk melakukan *deployment* software langsung ke PC/User ID pengguna secara remote.

### 3. Software Tidak Standar (Unapproved/Shadow IT)
Jika pengguna meminta aplikasi yang tidak ada di daftar standar perusahaan (misal: software edit video gratis yang tidak dikenal, alat konversi PDF online):
- **Tolak tiket secara sopan.**
- Jelaskan bahwa software tidak dievaluasi oleh IT Security.
- Tawarkan alternatif yang disetujui perusahaan (misal: sarankan Adobe Acrobat Standard yang sudah dilisensikan daripada situs konverter PDF web acak).

---

<a id="sop-010"></a>
## SOP-010: NEW EMPLOYEE ONBOARDING (IT PROVISIONING)

### 1. Trigger Otomatis
Proses *onboarding* IT idealnya dipicu oleh integrasi HR (Workday) ke Active Directory, di mana akun terbentuk otomatis (Status: Disabled) dengan format penamaan standar.

### 2. Tugas Agen Service Desk (H-3 sebelum masuk)
Meskipun otomatis, agen L1 harus memvalidasi kesiapan:
1. **Validasi Akun AD & Email:** Cek di ADUC apakah akun `Nama.Belakang` sudah terbentuk. Pastikan alamat email `nama.belakang@mitsubishi.co.id` sudah aktif di Exchange.
2. **Assign Lisensi:** Login ke Microsoft 365 Admin Center, pastikan lisensi **Microsoft 365 E3** dan paket tambahan (sesuai peran) telah dicentang.
3. **Tambahkan ke Grup:** Tambahkan pengguna ke *Distribution List (DL)* departemen terkait (misal: `DL-Finance-Team`) dan grup *Security* folder berbagi (File Server).
4. **Kordinasi Perangkat:** Cek tiket aset (SOP-008). Pastikan laptop siap di meja karyawan baru atau siap di-pickup saat *Onboarding Day* bersama HR.

### 3. Komunikasi Kredensial Awal
- Cetak "Welcome Letter" berisi panduan login, Temporary Password, dan panduan setting MFA (Merujuk ke SOP-002).
- Serahkan amplop bersegel berisi kredensial tersebut kepada tim HR (Onboarding Specialist) satu hari sebelum karyawan bergabung. Dilarang mengirim password awal ke email personal karyawan tanpa enkripsi.

---

<a id="sop-011"></a>
## SOP-011: ACCOUNT TERMINATION & OFFBOARDING

### 1. Tingkat Kekritisan: KRITIS (Security Compliance)
Offboarding yang gagal berisiko besar terhadap kebocoran data perusahaan. Eksekusi terminasi di IT harus dilakukan tepat pada waktu yang diinstruksikan oleh HR (berdasarkan jam kerja lokal atau *immediate termination*).

### 2. Prosedur Offboarding Standar (Resign Biasa)
Pada jam 17:00 di hari kerja terakhir karyawan:
1. Buka Active Directory Users and Computers (ADUC).
2. Temukan akun pengguna. Klik kanan -> **Disable Account**.
3. Pindahkan (Move) object *user* tersebut ke dalam *Organizational Unit (OU)*: `OU=Terminated Users,DC=mitsubishi,DC=local`.
4. Buka portal Microsoft 365 Admin. Cari pengguna.
5. Klik **Block Sign-in**.
6. Konversi *Mailbox* email pengguna menjadi **Shared Mailbox** untuk menyimpan data secara gratis.
7. Hapus penugasan Lisensi Microsoft 365 (Remove License) agar lisensi dapat dipakai karyawan lain.
8. Berikan delegasi akses (Full Access) ke Shared Mailbox tersebut kepada atasan/manager pengguna yang di-terminate, selama periode retensi maksimal 30 hari.

### 3. Prosedur Immediate Termination (Kasus Pelanggaran/Fraud)
- Segera lakukan **Disable AD** dan **Block Sign-In M365** seketika saat tiket "Immediate Action" diterima dari HR/Legal, tanpa menunggu jam pulang.
- Eksekusi *Remote Wipe* dari portal Intune jika laptop diduga dibawa kabur atau berisiko tinggi.
- Tutup seluruh akses VPN (SOP-001) dan SAP (kunci ID SAP melalui basis / SU01) dalam waktu maksimal 15 menit SLA.

---

<a id="sop-012"></a>
## SOP-012: TEAMS & M365 ACCESS MANAGEMENT

### 1. Tujuan
Mengatur siklus hidup, pembuatan, dan pengelolaan hak akses pada Microsoft Teams, SharePoint Online, dan OneDrive di ekosistem Mitsubishi.

### 2. Pembuatan Microsoft Teams / Channel Baru
Untuk mencegah "Teams Sprawl" (pembuatan grup Teams liar yang tidak terkelola), pembuatan ruang kerja Teams baru dibatasi.
1. Pengguna harus submit form di portal IT, menyebutkan Nama Teams, Deskripsi, dan minimal 2 nama Pemilik (Owner).
2. IT Agen mengevaluasi nama (Tidak boleh mengandung kata sensitif seperti "Gaji", "Confidential", atau duplikat).
3. Buat grup melalui Microsoft Teams Admin Center.
4. Terapkan *Naming Convention*: `[Dept Code] - [Nama Proyek]`. Contoh: `FIN - Q3 Tax Consolidation`.
5. Set atur *Privacy* ke **Private** (default perusahaan). Public Teams dilarang tanpa izin Direktur IT.

### 3. Pengelolaan Akses Eksternal (Guest Access)
Jika tim bisnis perlu mengundang vendor/konsultan luar ke dalam Teams:
- BSI IT Helpdesk harus memverifikasi bahwa akun eksternal tersebut berasal dari domain email perusahaan yang valid (bukan @gmail.com atau @yahoo.com).
- Jika disetujui, tambahkan email tamu ke Entra ID sebagai *Guest User*.
- Informasikan Pemilik Teams bahwa tamu akan terkena kebijakan audit setiap 90 hari (Access Review).

---

<a id="sop-013"></a>
## SOP-013: CORPORATE WIFI & 802.1X AUTHENTICATION

### 1. Arsitektur WiFi Mitsubishi
- **SSID Karyawan:** `MITSUBISHI-CORP` (Akses penuh ke Intranet & Internet, autentikasi aman EAP-TLS/PEAP via kredensial AD / Sertifikat perangkat).
- **SSID Tamu:** `MITSUBISHI-GUEST` (Hanya Internet, terisolasi penuh dari jaringan perusahaan, login via Web Captive Portal).

### 2. Penyelesaian Masalah `MITSUBISHI-CORP`
**Masalah: Laptop perusahaan tidak bisa menyambung WiFi.**
1. Pastikan laptop didistribusikan secara resmi oleh perusahaan. (Bring Your Own Device / BYOD dilarang keras di SSID Corporate).
2. Jika laptop gagal terhubung (Error: *Can't connect to this network*), ini biasanya karena sertifikat mesin (Machine Certificate) kedaluwarsa atau hilang.
3. **Tindakan Agen:**
   - Hubungkan PC ke jaringan LAN menggunakan kabel.
   - Buka Command Prompt.
   - Paksa pembaruan grup kebijakan: `gpupdate /force`
   - Buka `certlm.msc` -> *Personal* -> *Certificates*, pastikan ada sertifikat dengan nama PC yang di-issue oleh `Mitsubishi Internal CA`.
   - Jika tidak ada, jalankan request auto-enrollment atau hubungi L2 Network.

### 3. Permintaan Akses WiFi Guest
Jika tamu VIP/Vendor membutuhkan WiFi:
1. Karyawan yang mengundang (*Sponsor*) membuat tiket permintaan akun Guest WiFi maksimal H-1.
2. IT Service Desk men-generate kode akses sementara via *Cisco ISE / Aruba ClearPass Portal*.
3. Akses Guest WiFi diberikan maksimal berdurasi 1x24 Jam atau hingga jam 18:00 hari tersebut.
4. Kirimkan Username/Password Guest WiFi ke Sponsor.

---
**Catatan untuk AI RAG Pipeline:**
Dokumen ini disusun untuk dipecah (chunking) dan dimasukkan ke dalam Azure AI Search. 
Pastikan ukuran *chunking* diatur ke ~500 token dengan 50 token overlap untuk pengambilan konteks yang optimal sebagaimana disyaratkan dalam Project Framework BSI IT Desk.
