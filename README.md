Kurulum Kılavuzu
Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla uygulayınız.

1. Projeyi İndirin
Terminal veya Komut İstemi'ni açarak projeyi klonlayın:

git clone []

🔄 Çalışma Adımları
Mevcut Branch'leri Listeleme:
git branch

Yeni Branch Oluşturma ve Geçiş Yapma:
git checkout -b isim-gorev-adi
# Örnek: git checkout -b Berat-navbar-tasarimi

Farklı Bir Branch'e Geçiş Yapma:
git checkout branch-adi

1. Yeni Bir Göreve Başlarken:
git checkout -b isim-gorev-adi
# Örnek: git checkout -b Nur-login-formu

2. Kodları Kaydetme ve Gönderme
git add .
git commit -m "Yapılan işi özetleyen net bir mesaj yazın"
git push origin isim-gorev-adi

3. Birleştirme (Merge) Talebi: GitHub üzerinden "Compare & Pull Request" butonuna tıklayarak Proje Liderine birleştirme isteği gönderin.

4. Güncellemeleri Alma:
git checkout main
git pull origin main
Ardından kendi dalınıza dönüp çalışmaya devam edebilirsiniz:
git checkout kendi-dalim
git merge main
