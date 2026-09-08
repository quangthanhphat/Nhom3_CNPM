class AIRecommendationService:

    def __init__(self, service_repository):
        self.service_repository = service_repository

    def recommend(self, data):
        services = self.service_repository.list_all()

        film_format = data.get("film_format")
        processing_option = data.get("processing_option")
        scanning_quality = data.get("scanning_quality")
        printing_option = data.get("printing_option")
        max_price = data.get("max_price")
        max_turnaround = data.get("max_turnaround")

        recommendations = []

        for service in services:
            if service.status != "active":
                continue

            score = 0
            reasons = []

            # Film format
            if film_format and service.supported_film_formats:
                if film_format in service.supported_film_formats:
                    score += 3
                    reasons.append("Supports the selected film format")

            # Processing option
            if processing_option and service.processing_options:
                if processing_option in service.processing_options:
                    score += 3
                    reasons.append("Supports the selected processing option")

            # Scanning quality
            if scanning_quality and service.scanning_quality:
                if scanning_quality in service.scanning_quality:
                    score += 2
                    reasons.append("Supports the selected scanning quality")

            # Printing option
            if printing_option and service.printing_options:
                if printing_option in service.printing_options:
                    score += 2
                    reasons.append("Supports the selected printing option")

            # Price
            if max_price is not None:
                if service.price <= float(max_price):
                    score += 2
                    reasons.append("Within the selected budget")

            # Turnaround
            if max_turnaround is not None:
                if (
                    service.turnaround_time_max is not None
                    and service.turnaround_time_max <= int(max_turnaround)
                ):
                    score += 2
                    reasons.append("Within the selected turnaround time")

            if score > 0:
                recommendations.append({
                    "service": service,
                    "score": score,
                    "reasons": reasons
                })

        recommendations.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return recommendations[:10]