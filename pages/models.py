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
    """
        Das Modell KundeHatSoftware bildet einen Software-Paket welches vom Kunden genutzt wird, in der Datenbank ab.

        Attributes:
            standort   (Standort)    :    Das Standort, welches dieses Software-Paket nutzt.
            software   (Software)    :   Die Software die genutzt wird.
            version   (str)          :   Die Software-Version die bei dem Kunden vorliegt.
        Methods:
            __str__(self)   :   Ist eine Methode mit der sich die KundeHatSoftware selbst beschreibt.
    """

    standort = models.ForeignKey(Standort, on_delete=models.CASCADE)
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)

    def __str__(self):
        """
            Beschreibt die angesprochene Instanz.

            Parameters:
                self:   Die KundeHatSoftwareinstanz selbst.
            Returns:
                str (str): Name des Kunden konkateniert mit der Ortschaft des Standorts und der genutzten Software.
        """

        return self.standort.kunde.name + " - " + self.standort.ort + ": " + self.software.software_name


class Modul(models.Model):
    """
        Das Modell KundeHatSoftware bildet einen Software-Paket welches vom Kunden genutzt wird, in der Datenbank ab.

        Attributes:
            name       (Standort)    :    Der Name des Moduls.
            produkt    (Software)   :    Die Software der, das Modul angehört.
        Methods:
            __str__(self)   :   Ist eine Methode mit der sich die KundeHatSoftware selbst beschreibt.
    """

    name = models.CharField(max_length=50)
    produkt = models.ForeignKey(Software, on_delete=models.CASCADE)

    def __str__(self):
        """
            Beschreibt die angesprochene Instanz.

            Parameters:
                self:   Das Modulinstanz selbst.
            Returns:
                str (str): Der Name der Software konkateniert mit dem Namen des Moduls.
        """

        return str(self.produkt.software_name) + ": " + str(self.name)


class Ansprechpartner(models.Model):
    """
        Das Modell Ansprechpartner bildet einen Ansprechner eines Kunden, in der Datenbank ab.

        Attributes:
            vorname   (Standort)    :    Der Vorname des Ansprechpartners.
            nachname   (Software)   :    Der Nachname des Ansprechpartners.
            telefon_nr  (str)       :    Die Telefonnummer des Ansprechpartners.
            email       (Email)     :    Die Email-Adresse des Ansprechpartners
            standort    (Standort)  :    Der Standort, den der Ansprechpartner vertritt.
        Methods:
            __str__(self)   :   Ist eine Methode mit der sich die KundeHatSoftware selbst beschreibt.
    """

    vorname = models.CharField(max_length=100)
    nachname = models.CharField(max_length=100)
    telefon_nr = models.CharField(max_length=50)
    email = models.EmailField()
    standort = models.ForeignKey(Standort, on_delete=models.CASCADE)

    def __str__(self):
        """
            Beschreibt die angesprochene Ansprechpartner Instanz.

            Parameters:
                self:   Das Ansprechpartnerinstanz selbst.
            Returns:
                str (str): Der volle Name des Ansprechpartners.
        """

        return str(self.vorname) + " " + str(self.nachname)


class Lizenz(models.Model):
    """
        Das Modell Lizenz bildet die Lizenz eines Software-Produkts, in der Datenbank ab.

        Attributes:
            KundeHatSoftware    (KundeHatSoftware)  :   Das Software-Paket für welches die Lizenz gültig ist.
            license_key         (str)               :   Der Lizenzschlüssel der Software.
            detail              (str)               :   Eine Beschreibung zur Lizenz.
            gültig_von          (date)              :   Das Datum ab dem die Lizenz gültig ist.
            gültig_bis          (date)              :   Das Datum ab dem die Lizenz gültig ist.
            replace_key         (Lizenz)            :   Das Lizenz-Objekt, welches von dem aktuellen Lizenz
                                                        nach Ablauf der Gültigkeit ersetzt werden soll.
        Methods:
            __str__(self)   :   Ist eine Methode mit der sich die Lizenz selbst beschreibt.
    """

    KundeHatSoftware = models.ForeignKey(KundeHatSoftware, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    license_key = models.CharField(max_length=300)
    detail = models.TextField(null=True, default=None, blank=True)
    gültig_von = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    gültig_bis = models.DateField(auto_now_add=False, auto_now=False, blank=True)
    replace_key = models.OneToOneField('Lizenz', on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        """
            Beschreibt die angesprochene Lizenz Instanz.

            Parameters:
                self:   Das Lizenzinstanz selbst.
            Returns:
                str (str): Software-Produkt-Name konkateniert mit dem Modulnamen und das Lizenzschlüssel.
        """
        return self.KundeHatSoftware.__str__() + " - " + self.modul.name + self.license_key.__str__()


class Kundenlizenz(Lizenz):
    """
        Das Modell Kundenlizenz ist eine Vererbung des Lizenz-Models und bildet eine globale Lizenz eines Kunden ab.
        Es erbt alle Attribute und Methoden des Lizenzen-Models.
        Diese Lizenz kann von allen Standorten des Kunden genutzt werden.

        Attributes:
            kunde_id    (Kunde) :   Der Kunde, dem dieser Kundenlizenz gehört.
    """

    kunde_id = models.ForeignKey('Kunde', on_delete=models.CASCADE)


class Standortlizenz(Lizenz):
    """
        Das Modell Standortlizenz ist eine Vererbung des Lizenz-Models und bildet eine Lizenz eines spezifischen Standorts ab.
        Es erbt alle Attribute und Methoden des Lizenzen-Models.
        Diese Lizenz kann nur von diesem einen Standort genutzt werden.

        Attributes:
            standort_id    (Standort) :   Der Standort, dem dieser Standortlizenz gehört.
    """

    standort_id = models.ForeignKey('Standort', on_delete=models.CASCADE)
