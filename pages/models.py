from django.db import models
import datetime


class Kunde(models.Model):
    """
        Das Modell Kunde bildet den Kunden in der Datenbank ab.

        Attributes:
            name    (str)   :   Der Name des Kunden.
            vf_nummer (int) :   VF Nummer ist ein eindeutiger Schlüssel für Kunden die mehrere Standorte besitzen.
        Methods:
            __str__(self)   :   Ist eine mit der sich ein Kunden-Instanz selbst beschreibt.
    """
    name = models.CharField(max_length=50)
    vf_nummer = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        """
            Beschreibt die angesprochene Instanz.

            Parameters:
                self:   Die Kundeninstanz selbst.
            Returns:
                str (str): Name des angesprochenen Kundeninstanzes
        """
        return str(self.name)



class Standort(models.Model):
    """
        Das Modell Standort bildet ein Standort des Kunden in der Datenbank ab.

        Attributes:
            kunde    (Kunde)   :   Der Kunde, welchem der Standort angehört.
            name    (str)      :   Der Name des Standorts.
            telNr   (str)       :   Die Telefonnummer des Standorts.
            email   (str)       :   Die Email Adresse des Standorts.
            strasse (str)       :   Die Straße des Standorts.
            hausnr  (str)       :   Die Hausnummer des Standorts.
            plz     (str)       :   Die Postleitzahl der Ortschaft des Standorts.
            ort     (str)       :   Die Ortschaft in der, der Standort seinen Sitz hat.
            zeiten  (str)       :   Die Geschäftszeiten des Standorts.
        Methods:
            __str__(self)   :   Ist eine Methode mit der sich ein Standort-Instanz selbst beschreibt.
    """

    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    telNr = models.CharField(max_length=50)
    email = models.EmailField()
    strasse = models.CharField(max_length=100)
    hausnr = models.CharField(max_length=5)
    plz = models.CharField(max_length=10)
    ort = models.CharField(max_length=50)
    zeiten = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.kunde.name) + " " + str(self.name)


class Software(models.Model):
    """
        Das Modell Software bildet eine Software in der Datenbank ab.

        Attributes:
            software_name    (str)   :   Der Name der Software.
            version    (str)         :   Die aktuelle Version des Softwares.
            beschreibung   (str)     :   Die Beschreibung des Softwares.
        Methods:
            __str__(self)   :   Ist eine Methode mit der sich die Software selbst beschreibt.
    """
    software_name = models.CharField(max_length=50)
    version = models.CharField(max_length=10, default="NULL")
    beschreibung = models.TextField(default="")

    def __str__(self):
        """
            Beschreibt die angesprochene Instanz.

            Parameters:
                self:   Die Softwareinstanz selbst.
            Returns:
                str (str): Name der angesprochenen Software.
        """
        return self.software_name


class KundeHatSoftware(models.Model):
    standort = models.ForeignKey(Standort, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)

    def __str__(self):
        return self.standort.kunde.name + " - " + self.standort.ort + ": " + self.software.software_name


class Modul(models.Model):
    name = models.CharField(max_length=50)
    produkt = models.ForeignKey(Software, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.produkt.software_name) + ": " + str(self.name)


class Ansprechpartner(models.Model):
    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    telefon_nr = models.CharField(max_length=50)
    email = models.EmailField()
    standort = models.ForeignKey(Standort, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.vorname) + " " + str(self.nachname)


class Lizenz(models.Model):
    KundeHatSoftware = models.ForeignKey(KundeHatSoftware, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=300)
    detail = models.TextField(null=True, default=None, blank=True)
    gültig_von = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    gültig_bis = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    replace_key = models.OneToOneField('Lizenz', on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        return self.KundeHatSoftware.__str__() + " - " + self.modul.name + self.license_key.__str__()


class Kundenlizenz(Lizenz):
    kunde_id = models.ForeignKey('Kunde', on_delete=models.CASCADE)


class Standortlizenz(Lizenz):
    standort_id = models.ForeignKey('Standort', on_delete=models.CASCADE)
