SELECT id_EPN
FROM 
		(SELECT *
		FROM conversion_excel LEFT OUTER JOIN sellements
		ON sellements.id_EPN == conversion_excel.id_EPN AND sellements.id == conversion_excel.id)
WHERE txt_CR == "Non existant" AND (pdf_CR == "Texte"  AND  xls_CR == "Non existant")