package stock;

import java.time.LocalDate;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

public class PriceCalculator {

	private static final String SELECTED_FINANCIAL_FEED = FinancialFeed.CNNMoney;

	private List<Price> historicalPrices;
	private FinancialFeed feed;
	private boolean adjustByNews;

	private PriceCalculator(List<Price> historicalPrices, boolean adjustByNews) {
		this.historicalPrices = historicalPrices;
		this.adjustByNews = adjustByNews;
		if (adjustByNews) {
			this.feed = createNationalFinancialFeedFor(SELECTED_FINANCIAL_FEED);
		}

	}

	private NationalFinancialFeed createNationalFinancialFeedFor(String selectedFinancialFeed) {
		FinancialFeed subscribedFinancialFeed = FinancialFeed.subscribe(selectedFinancialFeed);
		return new NationalFinancialFeed(subscribedFinancialFeed);
	}

	public static PriceCalculator createPriceCalculator(List<Price> historicalPrices) {
		return new PriceCalculator(historicalPrices, false);
	}

	public static PriceCalculator createPriceCalculatorFedByNews(List<Price> historicalPrices) {
		return new PriceCalculator(historicalPrices, true);
	}

	public Double calculate(Stock stock) {
		Optional<Double> historicalAveragePrice = calculateHistoricalAveragePriceFor(stock);

		if (!historicalAveragePrice.isPresent()) {
			return 0.0;
		}

		return adjustByNewsIfNecessary(stock, historicalAveragePrice.get());
	}

	private Optional<Double> calculateHistoricalAveragePriceFor(Stock stock) {
		List<Price> pricesToBeCalculated = historicalPrices.stream()
				.filter(historicalPrice -> this.shouldBeCalculated(stock, historicalPrice))
				.collect(Collectors.toList());

		if (pricesToBeCalculated.isEmpty()) {
			return Optional.empty();
		}

		return calculateAverageOf(pricesToBeCalculated);
	}

	private boolean shouldBeCalculated(Stock stock, Price historicalPrice) {
		return hasRelationship(stock, historicalPrice) && isEffectiveHistorical(historicalPrice);
	}

	private Optional<Double> calculateAverageOf(List<Price> pricesToBeCalculated) {
		double sumOfPricesValues = pricesToBeCalculated.stream().mapToDouble(Price::getValue).sum();
		Double averagePrice = sumOfPricesValues / pricesToBeCalculated.size();
		return Optional.of(averagePrice);
	}

	private boolean isEffectiveHistorical(Price historicalPrice) {
		return historicalPrice.getCreationDate().isBefore(LocalDate.now());
	}

	private boolean hasRelationship(Stock stock, Price historicalPrice) {
		return Objects.equals(historicalPrice.getSymbol(), stock.getSymbol());
	}

	private Double adjustByNewsIfNecessary(Stock stock, Double averagePrice) {

		if (!adjustByNews) {
			return averagePrice;
		}

		return adjustAveragePriceByNews(stock, averagePrice);
	}

	private Double adjustAveragePriceByNews(Stock stock, Double averagePrice) {
		double sumOfNewsAdjustments = feed.fetch(stock.getSymbol()).stream().mapToDouble(News::getAdjustment).sum();
		return averagePrice + sumOfNewsAdjustments;
	}

}

class Price {

	public String getSymbol() {
		return null;
	}

	public LocalDate getCreationDate() {
		return null;
	}

	public Double getValue() {
		return null;
	}

}

class Stock {

	public String getSymbol() {
		return null;
	}

}

class FinancialFeed {

	public static final String CNNMoney = "CNNMoney";

	public static FinancialFeed subscribe(String feed) {
		return null;
	}

	public List<News> fetch(String symbol) {
		return null;
	}

}

class NationalFinancialFeed extends FinancialFeed {

	private FinancialFeed feed;

	public NationalFinancialFeed(FinancialFeed feed) {
		this.feed = feed;
	}

	@Override
	public List<News> fetch(String symbol) {
		return feed.fetch(symbol).stream().filter(this::isNational).collect(Collectors.toList());
	}

	private boolean isNational(News news) {
		return news.getSource() == NewsSource.NATIONAL;
	}

}

class News {
	public Double getAdjustment() {
		return null;
	}

	public NewsSource getSource() {
		return null;
	}
}

enum NewsSource {
	NATIONAL, INTERNATIONAL
}
