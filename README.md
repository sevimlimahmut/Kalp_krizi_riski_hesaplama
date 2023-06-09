Kodları indirdikten ve klasöre ayıkladıktan sonra Visual Studio Code ile açınız.
Flask-Web-App-Tutorial-main... içerisindeki main.py dosyasını çalıştırınız. Ama hatalar alacaksınız bunun sebebi bu web sitemizde kullandığımız makine öğrenmesi için gerekli olan datasetimizin bilgisayarımızda bulunma alanının farklı olmasıdır.
hata kısmında gelen bu hatayı bulun:File "c:\Users\Mahmut Sevimli\Desktop\Kalp_krizi_riski_hesaplama-main (2)\Kalp_krizi_riski_hesaplama-main\Flask-Web-App-Tutorial-main\Flask-Web-App-Tutorial-main\website\views.py", 
line 17, in <module>data=pd.read_csv(r"C:\Users\Mahmut Sevimli\Desktop\Flask-Web-App-Tutorial-main\Flask-Web-App-Tutorial-main\website\healthcare-dataset-stroke-data4.csv")
Flask-Web-App-Tutorial-main... içerisindeki ve  website içerisindeki  views.py dosyasını açınız ve bu kodun yazıldığı satırı bulunuz:data=pd.read_csv(r"C:\Users\Mahmut Sevimli\Desktop\Flask-Web-App-Tutorial-main\Flask-Web-App-Tutorial-main\website\healthcare-dataset-stroke-data4.csv")
Burada datasetin bilgisayarda bulunma yolunu gösteriyor ama dosyanın kaydedilme yeri değiştiği için burayı değiştirmelisiniz peki bunu nasıl yapacaksınız
3.satırdaki hata kodunun başında sizin dosya yolunuz bulunuyor tabi sizin bilgisayarınızda yine farklı olacaktır ben örnek olsun diye dosyayı farklı şekilde kaydetmiştim:"c:\Users\Mahmut Sevimli\Desktop\Kalp_krizi_riski_hesaplama-main (2)\Kalp_krizi_riski_hesaplama-main\Flask-Web-App-Tutorial-main\Flask-Web-App-Tutorial-main\website\views.py"
5.satırda bulduğun kodun yerine bunu yazınız, kaydediniz(ctrl+s) ve main.py üzerindenn projeyi tekrardann çalıştırınız: data=pd.read_csv(r"c:\Users\Mahmut Sevimli\Desktop\Kalp_krizi_riski_hesaplama-main (2)\Kalp_krizi_riski_hesaplama-main\Flask-Web-App-Tutorial-main\Flask-Web-App-Tutorial-main\website\healthcare-dataset-stroke-data4.csv")
 Running on http://127.0.0.1:5000 üzerinden sayfaya erişim şağlayabilirsiniz. 
 
